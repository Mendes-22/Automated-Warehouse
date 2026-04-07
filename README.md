# 🏗️ Smart WMS & Stacker Crane Control

**PLC: CODESYS V3.5 || Simulation: Factory I/O || Logic: Python & SQL**

An industrial-grade **Warehouse Management System (WMS)** solution that synchronizes high-level inventory logic with low-level automation. This project manages real-time storage (**Load**) and retrieval (**Unload**) cycles using a 3-axis Stacker Crane linked to a Python-based database backend.

## ⚡ Key Highlights

* **Integrated WMS Lifecycle:** Full management of pallet entry and exit, automated based on real-time database requests and sensor feedback.
* **PLC-Python Handshake:** Implementation of a robust synchronization protocol between CODESYS and Python to ensure zero-latency data exchange for target slotting.
* **Dynamic Pathfinding:** State-machine driven motion control to optimize X and Z axis travel time between the conveyor and high-density racking.
* **Automated Inventory Tracking:** Real-time feedback loop ensuring the physical pallet position always matches the digital SQL records.

## 📂 Project Structure & Hierarchy

The software is organized into modular folders to ensure reusability, scalability, and clean code maintenance:

* **`Warehouse/`**: The "Core Brain" (`FB_Warehouse`) that manages global system states and handles the Python communication handshake.
* **`Stacker_Crane/`**: Contains independent Function Blocks (`FB_Stacker_Load` and `FB_Stacker_Unload`) for dedicated motion profiles.
* **`Conveyor/` & `Height_Check/`**: Peripheral hardware drivers for entry validation and pallet transport.
* **`GVLs/`**: Centralized Global Variable Lists (`GVL_Python`, `GVL_Buffer_IDs`) for system-wide signal transparency.

## 🛠️ Technical Setup

* **Logic Architecture:** **Structured Text (ST)** for complex decision-making state machines and **Ladder Diagram (LD)** for prioritized hardware output mapping.
* **State Management:** Advanced execution flow using **ENUMs** and **CASE OF** structures to handle `WAIT_FOR_PYTHON`, `PICK_FROM_SHELVE`, and `DELIVER_TO_CONVEYOR` cycles.
* **Smart Output Mapping:** Integration of **SEL** blocks in the Main PRG to unify commands from multiple FBs into single hardware actuators.
* **Communication:** Seamless mapping of digital and analog I/Os between the PLC environment and the Factory I/O 3D simulation via OPC-UA/Shared Memory.

## 📸 In Action

> [!TIP]
> **Insert your Factory I/O simulation GIF or Screenshot here to showcase the Stacker Crane in motion!**
