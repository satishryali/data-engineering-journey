# dbt recall questions

Try these before reopening the lesson notes. These are pending practice prompts, not completed assessments.

1. Explain what dbt, PostgreSQL, and Airflow each do in our Airbnb pipeline.
2. PostgreSQL is stopped but laptop dbt still works. Can a model rebuild? What happened to the stored data?
3. Trace how dbt selects the project profile and then its target connection.
4. What must exist if target changes from dev to practice?
5. What changes when the profile schema changes from raw to analytics? When can a missing output schema be created?
6. What does dbt debug verify, and what does a successful check leave unverified?
7. Explain the difference between a table materialization and a view.
8. What does ref() tell dbt about two models?
9. What does version: 2 mean in a properties YAML file?
10. Does naming a file schema.yml create a database schema? Does a primary-key description create a constraint?
11. Predict unique and not_null results for IDs 1, 1, NULL, and explain the checks separately.
12. Does a failed data test remove or fix records?

13. With `target: dev` and three outputs, which connection does `dbt run` use? What changes with `--target prod`? What if `prod` is missing?
14. Can a target be named `practice`? Why should the profile contain only one `target` key?
15. Which must already exist: the PostgreSQL database, destination schema, or source table? What permissions does creation need?
16. A model reads `raw.raw_hosts` and the profile has `schema: analytics`. Identify the source, destination, and connection used.
17. How do a source declaration and `source()` tell dbt where to read? Does declaring a source load its data?
18. If the folder is renamed but `name: airbnb_dbt` stays the same, what is the project name? Does `dbt debug` edit it?
19. What does `version: '1.0.0'` in `dbt_project.yml` label? Compare it with `version: 2` in a properties file.
20. Write the command to load only `country_codes.csv` from several seeds. What type of data belongs in seeds?
21. Explain what happens to a query in `analyses/` during compilation and how you would get its result.
22. Where is `target/`, how is it generated, and how does it differ from `target: dev`?
23. What does `dbt test` display by default? How would you save failing records in PostgreSQL?
