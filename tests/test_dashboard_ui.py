from ui.dashboard import format_currency
from services.analytics_service import get_executive_kpis, get_priority_accounts_summary, get_funnel_distribution, get_industry_distribution


def test_currency_formatting():
    """Test formatting numbers into Indian Lakhs (L) or Crores (Cr)."""
    assert format_currency(50000.0) == "₹50,000"
    assert format_currency(4500000.0) == "₹45.0 Lakhs"
    assert format_currency(25000000.0) == "₹2.50 Cr"


def test_dashboard_data_providers():
    """Test analytics services feeding into the dashboard UI."""
    kpis = get_executive_kpis()
    assert "total_accounts" in kpis
    assert "pipeline_value" in kpis

    funnel = get_funnel_distribution()
    assert isinstance(funnel, list)

    industry = get_industry_distribution()
    assert isinstance(industry, list)

    priority = get_priority_accounts_summary(limit=5)
    assert isinstance(priority, list)
