import pytest
from models import Transaction, TransactionType
from repositories.transactions_impl_memory import InMemoryTransactionsRepository
from datetime import datetime

@pytest.fixture
def repo():
    """Fixture that returns a fresh repository before each test."""
    return InMemoryTransactionsRepository()

def test_save_and_find(repo):
    # prepare
    transaction = Transaction(
        id='test-t-id',
        amount=10,
        message="deposit",
        type=TransactionType.DEPOSIT,
        timestamp=datetime.now(),
        counterparty_iban="test",
        account_id="test"
    )

    # act
    saved_t = repo.save(transaction)
    found_t = repo.filter(account_id="test")

    # assert
    assert len(found_t) == 1
    assert found_t[0].id == "test-t-id"

def test_find_missing(repo):
    # act
    found = repo.filter(account_id="non-existent-id")

    #assert
    assert found == []
