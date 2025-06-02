Feature: AWS-S3 App JSON Schema Validation

  Background:
    Given I am on the welcome new user page
    And the saved JSON Schema is loaded for 'aws-s3' app
    And I fetch the templates API response for 'aws-s3' app

  Scenario: Validate live API response matches saved schema
    When I validate the response against the JSON Schema
    Then the response should conform to the schema
