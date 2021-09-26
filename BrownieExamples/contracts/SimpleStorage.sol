// SPDX-License-Idenntifier: MIT

pragma solidity >=0.6.6 <0.9.0;

contract SimpleStorage {
    uint256 favoriteNumber;

    struct Person {
        uint256 favoriteNumber;
        string name;
    }

    Person[] public people;
    mapping(string => uint256) public nameToFavoriteNumber;

    function store(uint256 favNum) public {
        favoriteNumber = favNum;
    }

    function retrieve() public view returns (uint256) {
        return favoriteNumber;
    }

    function AddPerson(string memory _name, uint256 _favNum) public {
        people.push(Person(_favNum, _name));
        nameToFavoriteNumber[_name] = _favNum;
    }
}
