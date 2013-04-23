--
-- PostgreSQL database dump
--

SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: feed; Type: TABLE; Schema: public; Owner: sumin; Tablespace: 
--

CREATE TABLE feed (
    id uuid NOT NULL,
    timestamp_fetched timestamp with time zone NOT NULL,
    feed_url character varying(255) NOT NULL,
    web_url character varying(255),
    version character varying(16),
    language character varying(16),
    title character varying(255),
    description text
);


ALTER TABLE public.feed OWNER TO sumin;

--
-- Name: feed_item; Type: TABLE; Schema: public; Owner: sumin; Tablespace: 
--

CREATE TABLE feed_item (
    id uuid NOT NULL,
    feed_id uuid NOT NULL,
    timestamp_published timestamp with time zone NOT NULL,
    timestamp_fetched timestamp with time zone NOT NULL,
    title character varying(255) NOT NULL,
    author character varying(255),
    link character varying(255),
    language character varying(16),
    description text,
    content text
);


ALTER TABLE public.feed_item OWNER TO sumin;

--
-- Name: feed_item_pkey; Type: CONSTRAINT; Schema: public; Owner: sumin; Tablespace: 
--

ALTER TABLE ONLY feed_item
    ADD CONSTRAINT feed_item_pkey PRIMARY KEY (id);


--
-- Name: feed_pkey; Type: CONSTRAINT; Schema: public; Owner: sumin; Tablespace: 
--

ALTER TABLE ONLY feed
    ADD CONSTRAINT feed_pkey PRIMARY KEY (id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--
