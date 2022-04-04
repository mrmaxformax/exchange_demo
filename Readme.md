
### My assumptions are:
1. I don't test how API handles incorrect requests and if it can return the valid status code:
- It always returns 200.
- Based on the requirements, the testing scope is just validation of the valid responses.
2. I use Pydantic library and I create the data classes for each endpoint. It helps to validate the response "by default":
- If the response has all fields.
- If the fields have correct data types.
  
3. I'm not sure if the requirement `Correctly handles the 2 factor authentication requirements.` is acceptable for
the demo version of API. I set MFA for both acc, but don't find any info if MFA is used for the demo API access. So I 
implement MFA only for the real acc. (Based on the info in the doc, it just required one special key in the payload).
4. The second problem is with `Retrieves open orders on the account and validates its content.` I was able to get the valid
response from both accounts, but for the real it does not have any data (no money - no order) . So I added
validation if the response has 0 values. But I was able successfully get info for demo API. Not 100% sure if it is what you 
really wanted :-) But because the code is ready, any tests can be easily added if it is required.

### How to run the tests.
1. Clone the project.
2. Add your keys to `secrets.ini` file.
3. From the project folder run: `make dev` to build the Docker.
4. Run the test (inside docker): `make run`. The test report will be generated "by default" after 
each test run.

### How to review the reports.
1. in the separate terminal run from local directory (not from the docker): `docker-compose up allure`
2. Open your browser and go-to: 
2a.`http://localhost:5050/allure-docker-service/projects/default` to see all reports.
2b.`http://localhost:5050/allure-docker-service/projects/default/reports/latest/index.html` to see last report.

### What if I can execute `make` command? 
- Just run required commands in your terminal. The commands can be found in Makefile. 



