import pytest
from fastapi.testclient import TestClient
from dependencies import get_accounts_repository, get_customers_repository
from app import app
from repositories.accounts_impl_memory import InMemoryAccountsRepository
from repositories.customers_impl_memory import InMemoryCustomersRepository
from models import Customer, Account

def override_accounts_repository():
    repository = InMemoryAccountsRepository()
    repository.save(
        account=Account(
            id="t1", 
            customer_id="cust-001", 
            name="t1", 
            balance=0.0
        )
    )
    repository.save(
        account=Account(
            id="t2", 
            customer_id="cust-001", 
            name="t2", 
            balance=10.0
        )
    )
    repository.save(
        account=Account(
            id="t3", 
            customer_id="cust-002", 
            name="t3", 
            balance=0.0
        )
    )
    return repository

def override_customers_repository():
    repository = InMemoryCustomersRepository()
    repository.save(customer=Customer(id="cust-001", name="tester", surname="tester"))
    repository.save(customer=Customer(id="cust-002", name="tester 2", surname="tester"))
    return repository

@pytest.fixture
def client():
    # Override the global dependency, to create a fresh repo for each test:
    app.dependency_overrides[get_accounts_repository] = override_accounts_repository
    app.dependency_overrides[get_customers_repository] = override_customers_repository
    with TestClient(app) as c:
        yield c
    # Clean up overrides
    app.dependency_overrides.clear()

def test_list_accounts(client):
    # act
    result = client.get(
        "/accounts/", 
    )

    # assert
    assert result.status_code == 200
    accounts = result.json()
    assert len(accounts) == 3

def test_filter_accounts(client):
    # act
    result = client.get(
        "/accounts/", 
        params={"customer_id": "cust-001"}
    )

    # assert
    assert result.status_code == 200
    accounts = result.json()
    assert len(accounts) == 2
    assert all(account["customer_id"] == "cust-001" for account in accounts)

