Feature: Ensure a database environment

  As a Sqema user
  I want to ensure my test/dev databases match my production databases
  So I can test and develop on them safely

  @fixture.sqlite
  Scenario: Development Mode Test
    Given we are using the general-test directory
    When we ensure the development environment
    Then the development tables match the sqema
    AND the development views match the sqema
    AND the development procedures match the sqema
    AND the development functions match the sqema
    AND the development indexes match the sqema
#    AND the development presettings match the sqema
#    AND the development postsettings match the sqema
#    AND the development other match the sqema