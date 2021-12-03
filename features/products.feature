Feature: The product store service back-end
    As a Product Store Owner
    I need a RESTful catalog service
    So that I can keep track of all my products

Background:
    Given the following products
        | name       | category | available |
        | iphone     | phone      | True      |
        | mac pro    | pc       | True      |
        | huawei     | phone     | False     |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Product Demo RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Product
    When I visit the "Home Page"
    And I set the "Name" to "Happy"
    And I set the "Category" to "Hippo"
    And I select "False" in the "Available" dropdown
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Category" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "Happy" in the "Name" field
    And I should see "Hippo" in the "Category" field
    And I should see "False" in the "Available" dropdown

Scenario: List all products
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see "iphone" in the results
    And I should see "mac pro" in the results
    And I should not see "huawei" in the results

Scenario: Search all phones
    When I visit the "Home Page"
    And I set the "Category" to "phone"
    And I press the "Search" button
    Then I should see "iphone" in the results
    And I should not see "huawei" in the results


Scenario: Update a Product
    When I visit the "Home Page"
    And I set the "Name" to "fido"
    And I press the "Search" button
    Then I should see "iphone" in the "Name" field
    And I should see "phone" in the "Category" field
    When I change "Name" to "iphone12"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "iphone12" in the "Name" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see "iphone12" in the results
    Then I should not see "iphone" in the results
