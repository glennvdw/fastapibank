import pytest
from unittest.mock import MagicMock
from services.services import TransactionService
from schemas import CreateTransactionRequest
from models import Transaction, TransactionType
from exceptions import AccountNotFound
from datetime import datetime

@pytest.fixture
def mock_transaction_repository():
    # We mock any dependencies to have more maintainable tests
    # Ideally each test should test only a single aspect 
    # and have only 1 possible cause of failure.
    return MagicMock()

@pytest.fixture
def mock_accounts_port():
    return MagicMock()

@pytest.fixture
def service(mock_transaction_repository, mock_accounts_port):
    return TransactionService(
        transaction_repository=mock_transaction_repository, 
        accounts_port=mock_accounts_port
    )

def test_create_transaction_unknown_account(service, mock_accounts_port):
    # prepare
    mock_accounts_port.get_account.return_value = None
    request = CreateTransactionRequest(
        account_id="test",
        amount=10,
        message="test",
        type=TransactionType.DEPOSIT,
        counterparty_iban="test"
    )

    # act / assert
    with pytest.raises(AccountNotFound):
        service.create_transaction(request)


def test_create_transaction_known_account(
    service, 
    mock_transaction_repository, 
    mock_accounts_port
    ):
    # prepare
    mock_accounts_port.get_account.return_value = {}
    mock_transaction_repository.filter.return_value = [
        Transaction(
            id="test",
            amount=10,
            message="test",
            type=TransactionType.DEPOSIT,
            timestamp=datetime.now(),
            account_id="test",
            counterparty_iban="test"
        )
    ] 
    mock_transaction_repository.save.side_effect = lambda t: t
    request = CreateTransactionRequest(
        account_id="test",
        amount=10,
        message="test",
        type=TransactionType.DEPOSIT,
        counterparty_iban="test"
    )

    # act
    result = service.create_transaction(request)

    # assert
    mock_transaction_repository.save.assert_called_once()
    mock_accounts_port.update_balance.assert_called_with(
        request.account_id, 
        10,
        result.timestamp,
    )
