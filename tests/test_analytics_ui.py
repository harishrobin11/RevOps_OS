from services.analytics_service import (
    get_funnel_conversion_rates,
    get_conversion_by_industry,
    get_conversion_by_lead_source,
    get_at_risk_opportunities_audit
)


def test_analytics_funnel_conversion_rates():
    """Test stage-to-stage conversion rates query."""
    rates = get_funnel_conversion_rates()
    assert isinstance(rates, list)
    assert len(rates) > 0
    assert "stage" in rates[0]
    assert "conversion_rate" in rates[0]


def test_analytics_performance_aggregations():
    """Test industry and lead source performance aggregations."""
    ind_perf = get_conversion_by_industry()
    assert isinstance(ind_perf, list)

    src_perf = get_conversion_by_lead_source()
    assert isinstance(src_perf, list)


def test_at_risk_audit_query():
    """Test at-risk opportunity audit query."""
    audit = get_at_risk_opportunities_audit()
    assert isinstance(audit, list)
