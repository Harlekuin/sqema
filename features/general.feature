Feature: Ensure a database environment

  As a Sqema user
  I want to ensure my test/dev databases match my production databases
  So I can test and develop on them safely

  @fixture.sqlite
  Scenario: Basic Functionality Test
    Given we are using the general-test directory
    When we ensure the test environment
    Then the test database matches the production database
