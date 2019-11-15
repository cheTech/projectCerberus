--
-- PostgreSQL database dump
--

-- Dumped from database version 11.5 (Ubuntu 11.5-1.pgdg18.04+1)
-- Dumped by pg_dump version 12.0

-- Started on 2019-11-12 10:18:15

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

--
-- TOC entry 196 (class 1259 OID 16388)
-- Name: projectcerberus_groups; Type: TABLE; Schema: public; Owner: projectcerberus
--

CREATE TABLE public.projectcerberus_groups (
    id integer NOT NULL,
    kvant text,
    "time" text,
    ownerid integer,
    deleted integer,
    dayofweek integer,
    cab integer
);


ALTER TABLE public.projectcerberus_groups OWNER TO projectcerberus;

--
-- TOC entry 197 (class 1259 OID 16396)
-- Name: projectcerberus_people; Type: TABLE; Schema: public; Owner: projectcerberus
--

CREATE TABLE public.projectcerberus_people (
    id integer NOT NULL,
    name text,
    groupid integer,
    deleted integer,
    photo text,
    pref text,
    face_encoding text
);


ALTER TABLE public.projectcerberus_people OWNER TO projectcerberus;


--
-- TOC entry 2806 (class 2606 OID 16395)
-- Name: projectcerberus_groups projectcerberus_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: projectcerberus
--

ALTER TABLE ONLY public.projectcerberus_groups
    ADD CONSTRAINT projectcerberus_groups_pkey PRIMARY KEY (id);


--
-- TOC entry 2808 (class 2606 OID 16403)
-- Name: projectcerberus_people projectcerberus_people_pkey; Type: CONSTRAINT; Schema: public; Owner: projectcerberus
--

ALTER TABLE ONLY public.projectcerberus_people
    ADD CONSTRAINT projectcerberus_people_pkey PRIMARY KEY (id);


-- Completed on 2019-11-12 10:18:16

--
-- PostgreSQL database dump complete
--

