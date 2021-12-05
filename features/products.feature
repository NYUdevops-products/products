Feature: The product store service back-end
    As a Product Store Owner
    I need a RESTful catalog service
    So that I can keep track of all my products

Background:
    Given the following products
        | name       | category |amount |likecount|status  |
        | iPhone     | phone    |1      |2        |Normal  |
        | Huawei     | phone    |2      |9        |Good    |
        | Nike       | shoe     |0      |5        |Unknown |
    # Given the following products
    #     |id | name       | category |amount | status  |likecount|
    #     | 1 | iPhone     | phone    |1      | Normal  |2        |
    #     | 2 | Huawei     | phone    |2      | Good    |9        | 
    #     | 3 | Nike       | shoe     |0      |Unknown  |5        | 

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Product Demo RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Product
    When I visit the "Home Page"
    And I set the "Name" to "Happy"
    And I set the "Category" to "Hippo"
    And I set the "Amount" to "1"
    And I set the "Likecount" to "1"
    And I select "Good" in the "Status" dropdown
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
    And I should see "1" in the "Amount" field
    And I should see "1" in the "Likecount" field
    And I should see "Good" in the "Status" dropdown

Scenario: List all products
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see "iPhone" in the results
    And I should see "Huawei" in the results
    And I should see "Nike" in the results

Scenario: Search all phones
    When I visit the "Home Page"
    And I set the "Category" to "phone"
    And I press the "Search" button
    Then I should see "iPhone" in the results
    And I should see "Huawei" in the results
    And I should not see "Nike" in the results

Scenario: Update a Product
    When I visit the "Home Page"
    And I set the "Name" to "iPhone"
    And I press the "Search" button
    Then I should see "iPhone" in the "Name" field
    And I should see "phone" in the "Category" field
    When I change "Name" to "OPPO"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "OPPO" in the "Name" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see "OPPO" in the results
    Then I should not see "iPhone" in the results

Scenario: List all products
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see "iPhone" in the results
    And I should see "Huawei" in the results
    And I should see "Nike" in the results


Scenario: Query product with name iPhone
    When I visit the "Home Page"
    And I set the "name" to "iPhone"
    And I press the "Retrieve" button
    Then I should see "iPhone" in the results
    And I should not see "Huawei" in the results
    And I should not see "Nike" in the results
