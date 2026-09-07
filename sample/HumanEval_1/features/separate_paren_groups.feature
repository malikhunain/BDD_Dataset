Feature: Separating nested parentheses groups
  As a string processing utility
  I want to separate balanced groups of nested parentheses from a string
  So that I can analyze individual balanced structures while ignoring whitespace

  Scenario: Multiple groups with internal and external spaces
    Given a paren string "( ) (( )) (( )( ))"
    When I separate the paren groups
    Then the result should be ['()', '(())', '(()())']

  Scenario: Nested groups with leading and trailing spaces
    Given a paren string " ( ( ) ) ( ) "
    When I separate the paren groups
    Then the result should be ['(())', '()']

  Scenario: Empty input string
    Given a paren string ""
    When I separate the paren groups
    Then the result should be []

  Scenario: Single deeply nested group
    Given a paren string "((()))"
    When I separate the paren groups
    Then the result should be ['((()))']

  Scenario: String containing only spaces
    Given a paren string "   "
    When I separate the paren groups
    Then the result should be []