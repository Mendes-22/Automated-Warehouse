import sqlite3
import time
from opcua import Client, ua

# --- CONFIGURATION ---
PLC_URL = "opc.tcp://127.0.0.1:4840"
DB_FILE = "warehouse.db"
BASE_PATH = "ns=4;s=|var|CODESYS Control Win V3 x64.Application.GVL_Python.Warehouse_Control"

def get_best_slot_from_db(box_type):
    """Find the nearest empty slot."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id FROM slots 
        WHERE occupied = 0 AND box_type = ? 
        ORDER BY id ASC LIMIT 1
    """, (box_type,))
    result = cursor.fetchone()
    if result:
        slot_id = result[0]
        cursor.execute("UPDATE slots SET occupied = 1 WHERE id = ?", (slot_id,))
        conn.commit()
        conn.close()
        return slot_id
    conn.close()
    return None

def unload_slot_in_db(slot_id):
    """Realease the slot in the SQL DB (Unload)."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # Check if is occupied before Unload
    cursor.execute("SELECT occupied FROM slots WHERE id = ?", (slot_id,))
    result = cursor.fetchone()
    if result and result[0] == 1:
        cursor.execute("UPDATE slots SET occupied = 0 WHERE id = ?", (slot_id,))
        conn.commit()
        conn.close()
        print(f"♻️ Slot {slot_id} is now FREE in Database.")
        return True
    conn.close()
    return False

def main():
    client = Client(PLC_URL)
    try:
        client.connect()
        print("🚀 Backend Engine ONLINE - MendesPLC Warehouse Manager")

        # --- NODES LOAD ---
        node_req_load = client.get_node(f"{BASE_PATH}.Request_Load")
        node_type     = client.get_node(f"{BASE_PATH}.Box_Type")
        node_target   = client.get_node(f"{BASE_PATH}.Target_Slot")
        node_ready    = client.get_node(f"{BASE_PATH}.Python_Load_Ready")

        # --- NODES UNLOAD --- 
        node_req_unload  = client.get_node(f"{BASE_PATH}.Request_Unload")
        node_unload_id   = client.get_node(f"{BASE_PATH}.Unload_ID")
        node_unload_ready = client.get_node(f"{BASE_PATH}.Python_Unload_Ready")

        while True:
            # --- LOAD LOGIC (ENTRY) ---
            if node_req_load.get_value():
                box_type = node_type.get_value()
                target_id = get_best_slot_from_db(box_type)
                
                if target_id:
                    node_target.set_value(ua.DataValue(ua.Variant(target_id, ua.VariantType.Int16)))
                    node_ready.set_value(ua.DataValue(ua.Variant(True, ua.VariantType.Boolean)))
                    print(f"✅ Assigned SLOT {target_id} for Box Type {box_type}")
                else:
                    print("⚠️ Warehouse FULL!")

                while node_req_load.get_value(): time.sleep(0.1) # Handshake
                node_ready.set_value(ua.DataValue(ua.Variant(False, ua.VariantType.Boolean)))

            # --- UNLOAD LOGIC (OUT) ---
            if node_req_unload.get_value():
                slot_to_empty = node_unload_id.get_value()
                print(f"📤 Unload requested for Slot: {slot_to_empty}")
                
                if unload_slot_in_db(slot_to_empty):
                    # Tells PLC that the DB is updated
                    node_unload_ready.set_value(ua.DataValue(ua.Variant(True, ua.VariantType.Boolean)))
                else:
                    print(f"❌ Error: Slot {slot_to_empty} is already empty!")

                while node_req_unload.get_value(): time.sleep(0.1) # Handshake
                node_unload_ready.set_value(ua.DataValue(ua.Variant(False, ua.VariantType.Boolean)))

            time.sleep(0.2)

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        client.disconnect()

if __name__ == "__main__":
    main()
