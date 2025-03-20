import pytest
from models import Customer, Account
from repositories.customers_impl_memory import InMemoryCustomersRepository

@pytest.fixture
def repo():
    """Fixture that returns a fresh repository before each test."""
    return InMemoryCustomersRepository()

def test_save_and_find(repo):
    # prepare
    acc = Account(
        id="test-acc-id", 
        customer_id="customer-123", 
        balance=100.0, 
        name="test-acc"
        )
    cus = Customer(
        id="test-cus-id", 
        name="Pieter-Jan", 
        surname="Beelen", 
        accounts=[acc]
    )

    # act
    saved_cus = repo.save(cus)
    found_cus = repo.find_by_id("test-cus-id")

    # assert
    assert saved_cus.id == "test-cus-id"
    assert saved_cus.name == "Pieter-Jan"
    assert saved_cus.surname == "Beelen"

    assert found_cus is not None
    assert found_cus.name == "Pieter-Jan"
    assert found_cus.surname == "Beelen"

def test_find_missing(repo):
    # act
    found_cus = repo.find_by_id("non-existent-id")

    # assert
    assert found_cus is None

def test_all(repo):
    # prepare
    account = Account(
        id="test-acc-id", 
        customer_id="customer-123", 
        balance=100.0, 
        name="test-acc"
    )
    repo._store[account.id] = account

    # act
    items = repo.all()

    # assert
    assert len(items) == 1
    assert items[0].id == "test-acc-id"