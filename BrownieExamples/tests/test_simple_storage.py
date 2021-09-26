# all test files need to be prefixed with test_
#
# run brownie tests
# ~brownie test
#
# run specific brownie test
# ~ brownie test -k <test function name>
#
# use the s flag for verbose output
# brownie test -s

from brownie import accounts, config, SimpleStorage


def test_deploy():
    # Arrange
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})

    # Act
    starting_value = simple_storage.retrieve()
    expected = 0

    # Assert
    assert starting_value == expected


def test_update_storage():
    # Arrange
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})

    # Act
    expected = 15
    simple_storage.store(expected, {"from": account})

    # Assert
    assert simple_storage.retrieve() == expected
