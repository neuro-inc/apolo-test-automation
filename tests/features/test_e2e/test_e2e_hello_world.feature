Feature: Apolo CLI Hello World Job Verification

  Background:
    Given the Apolo CLI client is installed

  @e2e
  Scenario: Run Hello World job and validate UI and CLI results
    Given "default" organization created via UI and I on the main page
    And I am logged in with Apolo CLI using an access token
    And I created "my-project" project via CLI
    When I run the 'Hello World' job via CLI

    When I open the Jobs page
    Then I should not see the 'Hello World' job in the running jobs list

    When I click the Show All Jobs button
    Then I should see the 'Hello World' job in the list
    And The 'Hello World' job status should be 'Successful'
