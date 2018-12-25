--------------------------------------------------------------------------

-- Creating trigger for creating work when theme curator, students are determined.

-- Trigger function
CREATE OR REPLACE FUNCTION create_theme_based_work()
  RETURNS trigger AS
$BODY$
BEGIN
    -- create new work based on theme
    INSERT INTO "Work"(date_start, theme_id)
    VALUES (now() AT TIME ZONE 'Europe/Moscow', NEW.id);

    RETURN NEW;
END;
$BODY$
LANGUAGE plpgsql;

-- Binding trigger
DROP TRIGGER IF EXISTS trigger_create_theme_based_work ON "Theme";
CREATE TRIGGER trigger_create_theme_based_work
  AFTER UPDATE
  ON "Theme"
  FOR EACH ROW
  WHEN ((OLD.* IS DISTINCT FROM NEW.*) AND -- execute only for updated rows
    (NEW.curator_id IS NOT NULL AND NEW.student_id IS NOT NULL AND  -- where curator, student are filled in
     NEW.date_acceptance IS NULL))  -- and do not need to insert into work
  EXECUTE PROCEDURE create_theme_based_work();

-- Trigger function for updating date_acceptance of filled theme
CREATE OR REPLACE FUNCTION update_theme_date_acceptance_based_work()
  RETURNS trigger AS
$BODY$
BEGIN
    UPDATE "Theme" SET date_acceptance = now() AT TIME ZONE 'Europe/Moscow'
    WHERE id = NEW.theme_id;

    RETURN NEW;
END;
$BODY$
LANGUAGE plpgsql;

-- Binding trigger
DROP TRIGGER IF EXISTS trigger_update_theme_date_acceptance_based_work ON "Work";
CREATE TRIGGER trigger_update_theme_date_acceptance_based_work
  AFTER INSERT
  ON "Work"
  FOR EACH ROW
  EXECUTE PROCEDURE update_theme_date_acceptance_based_work();

--------------------------------------------------------------------------

-- Procedure for clearing Suggestion table from REJECTED entries

CREATE OR REPLACE FUNCTION clear_suggestion_theme_rejected()
  RETURNS void AS
$BODY$
BEGIN
    DELETE FROM "Suggestion_theme"
    WHERE status_id in (
        SELECT id FROM "Suggestion_theme_status"
        WHERE name LIKE 'REJECTED_%'
    );
END;
$BODY$
LANGUAGE plpgsql;

--------------------------------------------------------------------------