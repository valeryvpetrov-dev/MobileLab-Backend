-- User: "SaaS-api_role_admin"
-- DROP USER "SaaS-api_role_admin";

CREATE USER "SaaS-api_role_admin" WITH
  LOGIN
  SUPERUSER
  INHERIT
  CREATEDB
  CREATEROLE
  NOREPLICATION;

COMMENT ON ROLE "SaaS-api_role_admin" IS 'Admin of SaaS-api_db.';

--------------------------------------------------------------------------

-- User: "SaaS-api_role_user"
-- DROP USER "SaaS-api_role_user";

CREATE USER "SaaS-api_role_user" WITH
  LOGIN
  NOSUPERUSER
  INHERIT
  NOCREATEDB
  NOCREATEROLE
  NOREPLICATION;

COMMENT ON ROLE "SaaS-api_role_user" IS 'User of SaaS-api_db.';

--------------------------------------------------------------------------

-- Database: SaaS-api_db_test

-- DROP DATABASE "SaaS-api_db_test";

CREATE DATABASE "SaaS-api_db_test"
    WITH
    OWNER = "SaaS-api_role_admin"
    ENCODING = 'UTF8'
    LC_COLLATE = 'Russian_Russia.1251'
    LC_CTYPE = 'Russian_Russia.1251'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

COMMENT ON DATABASE "SaaS-api_db_test"
    IS 'MobileLab-Backend project. Database for testing.';