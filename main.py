import asyncio
import logging
from haderlev_vbo import update_item_data

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

import sys

from automation_server_client._server import AutomationServer, WorkItemError
from automation_server_client._models import Workqueue, Credential, WorkItemStatus


from automation_server_client import AutomationServer

# simuleret data, som vi kunne få fra et excel ark eller system, som blot er en flad JSON. Disse oplysninger får vi standadiseret ved at køre update_item_data 
items = [
    {"cpr": "1234567890", "type": "adresseopslag", "note": "Test-item 1", "process_result": {"status": "OK"}},
    {"cpr": "1111111111", "type": "fødselsdato-check", "note": "Test-item 2"},
    {"cpr": "2222222222", "type": "myndighedsopslag", "note": "Test-item 3"},
    {"cpr": "3333333333", "type": "journalopslag", "note": "Test-item 4"},
]

# Dette er blot til at teste min funktion, for at se om den virker.

for i, item in enumerate(items):
    data_json = {}

    update_item_data(
        data_json,
        data_updates=item,
        log_entry={
            "message": "Item opdateret",
            "level": "INFO"
        }
    )

    items[i] = data_json  # ✅ OVERSKRIVER item i listen

ats = AutomationServer.from_environment()
queue = ats.workqueue()

# PRODUCER-MODE
for item in items:
    queue.add_item(data=item, reference=item["data"]["cpr"])

#print("Tilføjet items uden at processen complete’r noget.")
exit(0) #Exit gør, at den går ud af tifløj items, hvis man ikke gør det, så vil automation server automatisk complete det, fordi det er lavet sådan hvis alt er ok så bliver det complted



async def populate_queue(workqueue: Workqueue):
    logger = logging.getLogger(__name__)
    logger.info("Hello from populate workqueue!")


async def process_workqueue(workqueue: Workqueue):
    logger = logging.getLogger(__name__)
    logger.info("Hello from process workqueue!")

    for item in workqueue:
        with item:
            data = item.data

            try:
                # TODO: implement your work here
                pass
            except WorkItemError as e:
                logger.error(f"Error processing item: {data}. Error: {e}")
                item.fail(str(e))


if __name__ == "__main__":
    # Læs ATS_URL, ATS_TOKEN, osv.
    ats = AutomationServer.from_environment()

    # Få workqueue
    workqueue = ats.workqueue()

    # Queue management mode
    if "--queue" in sys.argv:
        workqueue.clear_workqueue(WorkItemStatus.NEW)
        asyncio.run(populate_queue(workqueue))
        exit(0)

    # Process mode
    asyncio.run(process_workqueue(workqueue))