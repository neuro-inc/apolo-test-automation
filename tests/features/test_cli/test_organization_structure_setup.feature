Feature: Organization Structure Setup

  Background:
    Given the Apolo CLI client is installed
    And I am on the welcome new user page
    And I am logged in with Apolo CLI using an access token

  @cli @bug-ENG-747
  Scenario: User creates a new organization
    Given the organizations list is empty
    When I add a new organization "My-organization" via apolo CLI
    And I list organizations via apolo CLI
    Then "My-organization" should be listed
