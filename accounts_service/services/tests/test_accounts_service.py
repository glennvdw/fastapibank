import pytest
from unittest.mock import MagicMock
from services.services import AccountsService
from schemas import CreateAccountRequest
from models import Account, Customer
from exceptions import CustomerNotFound

@pytest.fixture
def mock_accounts_repository():
    # We mock any dependencies to have more maintainable tests
    # Ideally each test should test only a single aspect 
    # and have only 1 possible cause of failure.
    return MagicMock()

@pytest.fixture
def mock_customers_repository():
    return MagicMock()

@pytest.fixture
def service(mock_accounts_repository, mock_customers_repository):
    return AccountsService(
        customers_repository=mock_customers_repository, 
        accounts_repository=mock_accounts_repository
    )

def test_create_account_unknown_customer(service, mock_customers_repository):
    # prepare
    mock_customers_repository.find_by_id.return_value = None
    request = CreateAccountRequest(customer_id="cust-001", name="test customer")

    # act / assert
    with pytest.raises(CustomerNotFound):
        service.create_account(request)


def test_create_account_known_customer(
    service, 
    mock_customers_repository, 
    mock_accounts_repository
    ):
    # prepare
    mock_customers_repository.find_by_id.return_value = Customer(
        id="cust-001", 
        name="glenn", 
        surname="vdw"
    )
    mock_accounts_repository.save.side_effect = lambda account: account
    request = CreateAccountRequest(customer_id="cust-001", name="test account")

    # act
    result = service.create_account(request)

    # assert
    mock_accounts_repository.save.assert_called_once()
    args, kwargs = mock_accounts_repository.save.call_args
    saved_account_arg = args[0]

    assert saved_account_arg.id is not None
    assert saved_account_arg.customer_id == "cust-001"
    assert saved_account_arg.balance == 0.0

# def test_get_account_not_found(service):
#     acc = service.get_account("bogus-id")
#     assert acc is None

# def test_create_and_retrieve_account(service):
#     # Create an account
#     request = CreateAccountRequest(customer_id="cust-001")
#     created = service.create_account(request)

#     # Now retrieve it
#     retrieved = service.get_account(created.id)
#     assert retrieved is not None
#     assert retrieved.id == created.id
#     assert retrieved.customer_id == "cust-001"
#     assert retrieved.balance == 0.0
