import time
from opcua import Client

# URL remains the same - Check OPC Configurator
url = "opc.tcp://127.0.0.1:4840"
client = Client(url)

try:
    client.connect()
    print("✅ Connection: ESTABLISHED!")
    
   # The path needs to be seen in the "Project Tree" in CODESYS
    node_path = "ns=4;s=|var|CODESYS Control Win V3 x64.Application.GVL_Python.Warehouse_Control.Request_Load"
    
    try:
        request_node = client.get_node(node_path)
        print(f"📍 Success! Node found.")
        print(f"📦 Request_Load Value: {request_node.get_value()}")
    except:
        print("❌ Direct Path failed. Let's browse the Application...")
        objects = client.get_objects_node()
      
        # This will list everything inside "Application" to find the REAL name
        for child in objects.get_children():
            if "Application" in child.get_browse_name().Name:
                print(f"--- Nodes inside {child.get_browse_name().Name} ---")
                for sub in child.get_children():
                    print(f"Found: {sub.get_browse_name().Name} | ID: {sub.nodeid.to_string()}")

    client.disconnect()

except Exception as e:
    print(f"❌ Connection Error: {e}")
