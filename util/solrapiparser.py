from django.views.generic import TemplateView
from django.http import JsonResponse
from django.conf import settings
import pysolr
import logging
import datetime
import math
from util.logmanager import logz
log = logz()

logger = logging.getLogger(__name__)

SOLR_HOST = settings.__dict__.get('SOLR_HOST', "localhost")
SOLR_HOST_PORT = settings.__dict__.get('SOLR_HOST_PORT', "8983")


class SolrAPIParser():
    """
    http://localhost:8000/api/v1/{id}/search ({id} is collections name)
    &fl=id,domain_s
    &start=4
    &rows=50
    &fq__status_i=404&fq__domain_s=scienceblogs.com
    &fq__created_dt=[2015-01-11T00:00:00Z TO 2018-04-11T00:00:00Z]
    http://localhost:8000/api/v1/{id}/search?page=1&facet_fields=status_i,domain_s&fl=id,url_s,created_dt&fq__created_dt=[2018-03-15T12:22:45Z%20TO%202018-03-15T12:22:50Z]
    """
    cached_solr_connections = {}
    DEFAULT_ROWS_COUNT = 10

    def extract_facet_fields(self, url_query):
        facet_fields = url_query.get('facet_fields', "")
        if "facet_fields" in url_query:
            del url_query['facet_fields']

        facet_date_field = url_query.get('facet_date_field')
        if "facet_date_field" in url_query:
            del url_query['facet_date_field']
        facet_date_field_start = url_query.get('facet_date_field_start')
        if "facet_date_field_start" in url_query:
            del url_query['facet_date_field_start']

        facet_date_field_end = url_query.get('facet_date_field_end')
        if "facet_date_field_end" in url_query:
            del url_query['facet_date_field_end']

        facet_fields_dict = {}
        if len(facet_fields) > 0 or facet_date_field:
            facet_fields_dict['facet'] = "on"
            facet_limit = int(url_query.get('facet_limit', 10))
            if 'facet_limit' in url_query:
                del url_query['facet_limit']

            facet_page = int(url_query.get('facet_page', 1))
            if 'facet_page' in url_query:
                del url_query['facet_page']
            facet_fields_dict['facet.limit'] = facet_limit
            facet_fields_dict['facet.offset'] = facet_limit * (facet_page - 1)

        if len(facet_fields) > 0:
            facet_fields_dict['facet.field'] = facet_fields.split(",")
        if facet_date_field:
            facet_fields_dict['facet.range'] = facet_date_field
            if facet_date_field_start is None:
                facet_fields_dict['facet.range.start'] = 'NOW/MONTH'
            else:
                facet_fields_dict['facet.range.start'] = facet_date_field_start
            if facet_date_field_end is None:
                facet_fields_dict['facet.range.end'] = 'NOW/MONTH+1MONTH'
            else:
                facet_fields_dict['facet.range.end'] = facet_date_field_end

            facet_fields_dict['facet.range.gap'] = '+1DAY'
        return facet_fields_dict

    def query_parse_nofacet(self, request, q):
        url_query_dict = request.GET.copy()
        url_dic_d = dict(url_query_dict)
        log.info('url_query_dict:%s' % url_query_dict)

        rows = url_query_dict.get("rows", self.DEFAULT_ROWS_COUNT)
        log.info('rows:%s' % rows)
        if "rows" in url_query_dict:
            del url_query_dict['rows']

        start = url_query_dict.get('start', 0)
        if "start" in url_query_dict:
            del url_query_dict['start']

        fl = url_query_dict.get('fl', '*').split(",")
        log.info('fl:%s' % fl)

        if fl == ["*"]:
            fl = []
        if "fl" in url_query_dict:
            del url_query_dict['fl']

        df = url_query_dict.get('df', '*').split(",")
        log.info('df:%s' % df)

        if df == ["*"]:
            df = []
        if "df" in url_query_dict:
            del url_query_dict['df']

        solr_kwargs = {
            "rows": int(rows),
            "start": int(start),
        }

        if 'indent' in url_query_dict:
            solr_kwargs['indent'] = 'true'
            del url_query_dict['indent']

        facet_fields_dict = self.extract_facet_fields(url_query_dict)
        solr_kwargs.update(facet_fields_dict)

        if len(fl) > 0:
            solr_kwargs["fl"] = fl

        if len(df) > 0:
            solr_kwargs["df"] = df

        field_queries_dict = {}

        if 'sort' in url_dic_d:
            solr_kwargs['sort'] = url_dic_d.get('sort', '')

        if 'group' in url_dic_d:
            g = url_dic_d.get('group', False)
            if g:
                if g[0] == 'false':
                    solr_kwargs['group'] = False
                elif g[0] == 'true':
                    solr_kwargs['group'] = True
                else:
                    solr_kwargs['group'] = False

        if 'hl' in url_dic_d:
            h = url_dic_d.get('hl', False)
            if h:
                if h[0] == 'on':
                    solr_kwargs['hl'] = True
                elif h[0] == 'off':
                    solr_kwargs['hl'] = False
                else:
                    solr_kwargs['hl'] = False
            else:
                solr_kwargs['hl'] = False

        if 'facet' in url_dic_d:
            f = url_dic_d.get('facet', False)
            if f:
                if f[0] == 'false':
                    solr_kwargs['facet'] = False
                elif f[0] == 'true':
                    solr_kwargs['facet'] = True
                else:
                    solr_kwargs['facet'] = False

        if 'fq' in url_dic_d:
            solr_kwargs['fq'] = url_dic_d.get('fq', [])
        # for k, v in url_query_dict.items():
        #     if k.startswith("fq__"):
        #         field_queries_dict[k.replace("fq__", "")] = v
        #     else:
        #         field_queries_dict[k] = v

        if len(field_queries_dict.keys()) == 0:
            field_queries_dict = {"*": "*"}

        solr_kwargs.update(field_queries_dict)
        return solr_kwargs


    # def extract_from_query(self, request):
    #     url_query_dict = request.GET.copy()
    #     print('url_query_dict:%s' % url_query_dict)
    #
    #     rows = url_query_dict.get("rows", self.DEFAULT_ROWS_COUNT)
    #     print('rows:%s' % rows)
    #     if "rows" in url_query_dict:
    #         del url_query_dict['rows']
    #
    #     page = url_query_dict.get('page', 1)
    #     if "page" in url_query_dict:
    #         del url_query_dict['page']
    #
    #     fields = url_query_dict.get('fl', '*').split(",")
    #     print('fl:%s' % fields)
    #
    #     if fields == ["*"]:
    #         fields = []
    #     if "fl" in url_query_dict:
    #         del url_query_dict['fl']
    #
    #     solr_kwargs = {
    #         "rows": int(rows),
    #         "start": int(rows) * (int(page) - 1),
    #     }
    #
    #     if 'indent' in url_query_dict:
    #         solr_kwargs['indent'] = 'true'
    #         del url_query_dict['indent']
    #     facet_fields_dict = self.extract_facet_fields(url_query_dict)
    #     solr_kwargs.update(facet_fields_dict)
    #     if len(fields) > 0:
    #         solr_kwargs["fl"] = fields
    #
    #     field_queries_dict = {}
    #     for k, v in url_query_dict.items():
    #         if k.startswith("fq__"):
    #             field_queries_dict[k.replace("fq__", "")] = v
    #         else:
    #             field_queries_dict[k] = v
    #
    #     if len(field_queries_dict.keys()) == 0:
    #         field_queries_dict = {"*": "*"}
    #     search_query = " AND ".join(["{}:{}".format(k, v) for k, v in field_queries_dict.items()])
    #
    #     solr_kwargs["q"] = search_query
    #     return solr_kwargs, search_query

    def convert_facets_field_to_dict(self, data):
        data_cleaned = []
        first = True
        first_word = None
        for i, k in enumerate(data):
            if first:
                first_word = k
                first = False
            else:
                d = {
                    first_word: k
                }
                data_cleaned.append(d)
                first_word = None
                first = True
        return data_cleaned

    def clean_docs(self, docs):
        cleaned_docs = []
        for doc in docs:
            cleaned_doc = {}
            for k, v in doc.items():
                if k.endswith("_dt"):
                    date_string = v.strip("Z")
                    if "." in date_string:
                        date_string = date_string.split(".")[0]
                    date_object = datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S')
                    cleaned_doc[k] = date_object
                else:
                    cleaned_doc[k] = v
            cleaned_docs.append(cleaned_doc)

        return cleaned_docs

    def clean_data(self, data):
        cleaned_data = data
        for k, v in data.get('facets', {}).get('facet_fields', {}).items():
            cleaned_data['facets']['facet_fields'][k] = self.convert_facets_field_to_dict(v)

        for k, v in data.get('facets', {}).get('facet_ranges', {}).items():
            cleaned_data['facets']['facet_ranges'][k]['counts'] = self.convert_facets_field_to_dict(v['counts'])

        cleaned_data['docs'] = self.clean_docs(data.get("docs", []))
        return cleaned_data

#     def get(self, request, *args, **kwargs):
#         collection_name = kwargs['collection_name']
#         print('collection_name:%s' % collection_name)
#         print('kwargs:%s' % kwargs.keys())
#
#         # if collection_name not in self.cached_solr_connections.keys():
#         #     solr_connection = pysolr.Solr('http://{}:{}/solr/{}/'.format(SOLR_HOST, SOLR_HOST_PORT, collection_name),
#         #                                   timeout=10)
#         #     self.cached_solr_connections[collection_name] = solr_connection
#         # else:
#         #     solr_connection = self.cached_solr_connections.get(collection_name)
#
#         solr_kwargs, search_query = self.extract_from_query()
#         logger.info(solr_kwargs)
#
#         try:
#             # data = solr_connection.search(**solr_kwargs).__dict__
#             data = {}
#         except Exception as e:
#             print(e)
#             return JsonResponse({"message": "Failed to connect to the collection: {}".format(collection_name)},
#                                 status=400)
#
#         # print(data['raw_response'])
#         if "raw_response" in data.keys():
#             del data['raw_response']
#         cleaned_data = self.clean_data(data)
#         # cleaned_data['docs_total_pages'] = math.ceil(int(cleaned_data['hits']) / int(
#         #     self.request.GET.get("rows", self.DEFAULT_ROWS_COUNT)))
#
#         # return JsonResponse({"data": cleaned_data, "message": "Ok"}, status=200)
#         return JsonResponse({"data": "1111", "message": "Ok"}, status=200)
# #     e.g. http://127.0.0.1:8000/api/indexing/solr/test_analytics?fl=id,sales_i,expenses_i,savings_i,share_value_i,created_dt&rows=1000&fq__created_dt=[2020-12-28T00:00:00Z%20TO%202021-01-3T00:00:00Z]&facet_date_field_start=2020-12-28T00:00:00Z&facet_date_field_end=2021-01-3T00:00:00Z

#
# class SolrFacetAPIView(TemplateView):
#     cached_solr_connections = []
#
#     def get(self, request, *args, **kwargs):
#         collection_name = kwargs['collection_name']
#         if collection_name not in self.cached_solr_connections.keys():
#             solr_connection = pysolr.Solr('http://{}:{}/solr/{}/'.format(SOLR_HOST, SOLR_HOST_PORT, collection_name),
#                                           timeout=10)
#             self.cached_solr_connections[collection_name] = solr_connection
#         else:
#             solr_connection = self.cached_solr_connections.get(collection_name)
#
#         # ?q=*:*&facet.range=created_dt&facet=true&facet.range.start=NOW/MONTH&facet.range.end=NOW/MONTH%2B1MONTH&facet.range.gap=%2B1DAY
#         return JsonResponse({"data": {}, "message": "ok"}, status=200)
