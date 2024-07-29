-- https://app.snowflake.com/marketplace/listing/GZSTZIDI09G/predicthq-intelligent-event-data-attended-events-munich-sample

-- It creates one view:
-- GHIMMOHMOH_SAMPLE.MUNICH_EVENTSEVENTS__ATTRIBUTES_LIMITED:
--    A subset of MUNICH_EVENTS__economic_essentials.cybersyn.financial_institution_attributes:
--    Totals for assets, real estate loans, securities, deposits; % of deposits insured; total employees


-- Create a dedicated database and schema for the new views
CREATE DATABASE IF NOT EXISTS GHIMMOHMOH_SAMPLE;
CREATE SCHEMA IF NOT EXISTS GHIMMOHMOH_SAMPLE.MUNICH_EVENTS;

-- Create the limited attributes view
CREATE VIEW IF NOT EXISTS GHIMMOHMOH_SAMPLE.MUNICH_EVENTS.EVENTS_ATTRIBUTES_LIMITED AS
SELECT * from INTELLIGENT_EVENT_DATA_ATTENDED_EVENTS_MUNICH__SAMPLE.PREDICTHQ.PREDICTHQ_ATTENDED_EVENTS_MUNICH e
where phq_attendance is not NULL;


-- Confirm the view was created correctly - should show 6 rows with variable name and definition
SELECT * FROM GHIMMOHMOH_SAMPLE.MUNICH_EVENTSEVENTS__ATTRIBUTES_LIMITED;

CREATE VIEW IF NOT EXISTS GHIMMOHMOH_SAMPLE.PUBLIC.VIEW3 AS
SELECT TITLE, CATEGORY, "DESCRIPTION", EVENT_START, EVENT_END, GEO, PREDICTED_EVENT_SPEND_HOSPITALITY, PREDICTED_EVENT_SPEND_TRANSPORTATION, FORMATTED_ADDRESS, PHQ_ATTENDANCE, PHQ_LABELS  from INTELLIGENT_EVENT_DATA_ATTENDED_EVENTS_MUNICH__SAMPLE.PREDICTHQ.PREDICTHQ_ATTENDED_EVENTS_MUNICH

