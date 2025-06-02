Feature: Apolo CLI Login

  Background:
    Given the Apolo CLI client is installed

  @cli
  Scenario: User logs in to Apolo CLI and verifies login success
    Given I am on the welcome new user page
    When I login to Apolo CLI with an auth token
    Then I should see successful login confirmation in CLI output
    And the valid organization and project should be displayed in CLI output
