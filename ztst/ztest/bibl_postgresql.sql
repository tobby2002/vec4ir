-- Drop table

-- DROP TABLE public.bibl;

CREATE TABLE public.bibl (
	bbid int4 NOT NULL,
	bible_bcn varchar(20) NOT NULL,
	"content" text NULL,
	book varchar(3) NOT NULL,
	chapter int4 NOT NULL,
	"number" int4 NULL,
	ebible_bcn varchar(20) NOT NULL,
	econtent text NULL
);

-- Permissions

ALTER TABLE public.bibl OWNER TO saleor;
GRANT ALL ON TABLE public.bibl TO saleor;

