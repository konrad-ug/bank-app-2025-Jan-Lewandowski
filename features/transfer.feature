Feature: Money transfer

Scenario: Successful getting Money
    Given Account registry is empty
    When I create an account using name: "kurt", last name: "cobain", pesel:"89092909246"
    When I send a transfer request to pesel "89092909246" with amount:"700" type:"incoming"
    When I send a transfer request to pesel "89092909246" with amount:"300" type:"incoming"
    When I send a transfer request to pesel "89092909246" with amount:"100" type:"outgoing"
    Then Account with pesel "89092909246" has 900 cash
Scenario: Sending more money than the user has
    Given Account registry is empty
    When I create an account using name: "kurt", last name: "cobain", pesel:"89092909246"
    When I send a transfer request to pesel "89092909246" with amount:"700" type:"outgoing"
    Then Account with pesel "89092909246" has -700 cash