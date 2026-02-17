"""Tests for Investigator LangChain tools."""

from unittest.mock import MagicMock

from aegis.agents.investigator_tools import make_tools


class TestMakeTools:
    def test_returns_five_tools(self):
        mock_connector = MagicMock()
        mock_db = MagicMock()
        tools = make_tools(mock_connector, mock_db)
        assert len(tools) == 5

    def test_list_schemas_calls_connector(self):
        mock_connector = MagicMock()
        mock_connector.list_schemas.return_value = ["public", "staging"]
        mock_db = MagicMock()
        tools = make_tools(mock_connector, mock_db)
        list_schemas = tools[0]
        result = list_schemas.invoke({})
        mock_connector.list_schemas.assert_called_once()
        assert result == ["public", "staging"]

    def test_list_tables_calls_connector(self):
        mock_connector = MagicMock()
        mock_connector.list_tables.return_value = [{"name": "users", "type": "BASE TABLE", "schema": "public"}]
        mock_db = MagicMock()
        tools = make_tools(mock_connector, mock_db)
        list_tables = tools[1]
        result = list_tables.invoke({"schema_name": "public"})
        mock_connector.list_tables.assert_called_once_with("public")

    def test_inspect_columns_calls_fetch_schema(self):
        mock_connector = MagicMock()
        mock_connector.fetch_schema.return_value = [
            {"name": "id", "type": "INTEGER", "nullable": False, "ordinal": 1}
        ]
        mock_db = MagicMock()
        tools = make_tools(mock_connector, mock_db)
        inspect = tools[2]
        result = inspect.invoke({"schema_name": "public", "table_name": "users"})
        mock_connector.fetch_schema.assert_called_once_with("public", "users")

    def test_check_freshness_returns_dict(self):
        mock_connector = MagicMock()
        mock_connector.fetch_last_update_time.return_value = None
        mock_db = MagicMock()
        tools = make_tools(mock_connector, mock_db)
        check_freshness = tools[3]
        result = check_freshness.invoke({"schema_name": "public", "table_name": "users"})
        assert result["has_timestamp"] is False

    def test_get_lineage_without_graph(self):
        mock_connector = MagicMock()
        mock_db = MagicMock()
        tools = make_tools(mock_connector, mock_db, lineage_graph=None)
        get_lineage = tools[4]
        result = get_lineage.invoke({"table_name": "public.users"})
        assert result == {"upstream": [], "downstream": []}
