import pytest
from models import Account
from repositories.accounts_impl_memory import InMemoryAccountsRepository

@pytest.fixture
def repo():
    """Fixture that returns a fresh repository before each test."""
    return InMemoryAccountsRepository()

def test_save_and_find(repo):
    # prepare
    acc = Account(
        id="test-acc-id", 
        customer_id="customer-123", 
        balance=100.0, 
        name="acc-1"
    )

    # act
    saved_acc = repo.save(acc)
    found_acc = repo.find_by_id("test-acc-id")

    # assert
    assert saved_acc.id == "test-acc-id"
    assert saved_acc.balance == 100.0

    assert found_acc is not None
    assert found_acc.id == "test-acc-id"
    assert found_acc.customer_id == "customer-123"
    assert found_acc.balance == 100.0

def test_find_missing(repo):
    # act
    found_acc = repo.find_by_id("non-existent-id")

    #assert
    assert found_acc is None
