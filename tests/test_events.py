from mpt_extension_sdk.core.events.dataclasses import Event

from swo_playground.events import process_order_fulfillment


def test_process_order_fulfillment(mocker, mock_mpt_client, caplog):
    mock_purchase_pipeline_run = mocker.patch(
        "swo_playground.steps.purchase_pipeline.run", autospec=True
    )
    mock_data = mocker.Mock(order_id="fake-order-id")
    mock_event = mocker.Mock(data=mock_data, spec=Event)

    process_order_fulfillment(mock_mpt_client, mock_event)  # act

    mock_purchase_pipeline_run.assert_called_once_with(mock_mpt_client, mock_data)
    assert "fake-order-id - Order fulfilling..." in caplog.text
    assert "fake-order-id - Order fulfilled." in caplog.text
