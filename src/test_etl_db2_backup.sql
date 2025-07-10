--
-- PostgreSQL database dump
--

-- Dumped from database version 16.2
-- Dumped by pg_dump version 17.5

-- Started on 2025-06-19 21:16:26

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 216 (class 1259 OID 51855)
-- Name: item_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.item_type (
    item_type_name text
);


ALTER TABLE public.item_type OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 51850)
-- Name: sales_txn; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sales_txn (
    id text,
    txn_type text,
    description text,
    item_type_name text,
    customer_id text,
    qty text,
    txn_date text
);


ALTER TABLE public.sales_txn OWNER TO postgres;

--
-- TOC entry 4835 (class 0 OID 51855)
-- Dependencies: 216
-- Data for Name: item_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.item_type (item_type_name) FROM stdin;
handheld
tower
server
\.


--
-- TOC entry 4834 (class 0 OID 51850)
-- Dependencies: 215
-- Data for Name: sales_txn; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sales_txn (id, txn_type, description, item_type_name, customer_id, qty, txn_date) FROM stdin;
ord1	retail	new order	handheld	c1	200	2025-04-25
ord1	retail	new order	laptop	c1	200	2025-04-25
\.


-- Completed on 2025-06-19 21:16:26

--
-- PostgreSQL database dump complete
--

