# 🏗️ Smart WMS & Stacker Crane Control

**PLC: CODESYS V3.5 || Simulation: Factory I/O || Logic: Python & SQL**

An industrial-grade **Warehouse Management System (WMS)** that synchronizes high-level inventory logic with low-level automation. This project features a **Weight-Balanced & Path-Optimized Strategy**, ensuring structural stability by placing heavy items on lower levels while minimizing travel time for all storage and retrieval operations.

## ⚡ Key Highlights

* **Strategic Slotting & Path Optimization:** Dynamic assignment of slots based on item height/weight. The system is programmed to prioritize the **nearest available location**, reducing X-Z axis travel distance and increasing overall operational throughput.
* **Weight-Balanced Storage:** Automatic classification of items to ensure heavier loads are stored on lower shelves, maintaining the racking system's structural integrity.
* **Integrated WMS Lifecycle:** Full management of pallet entry and exit, automated based on real-time database requests and sensor feedback.
* **PLC-Python Handshake:** Implementation of a robust synchronization protocol between CODESYS and Python to ensure zero-latency data exchange for target slotting.
* **Conflict-Free Actuation:** Advanced logic to prevent "Double Coil" conflicts by centralizing hardware commands through prioritized **OR logic** and **Selection (SEL)** blocks.

## 📂 Project Structure & Hierarchy

The software is organized into modular folders to ensure reusability and clean code maintenance:

* **`Warehouse/`**: The "Core Brain" (`FB_Warehouse`) that manages global system states and handles the Python communication handshake.
* **`Stacker_Crane/`**: Contains independent Function Blocks (`FB_Stacker_Load` and `FB_Stacker_Unload`) for dedicated motion profiles.
* **`Conveyor/` & `Height_Check/`**: Hardware drivers for entry validation, weight/height classification, and pallet transport.

## 🛠️ Technical Implementation

* **Logic:** **Structured Text (ST)** for decision-making state machines (Pathfinding & Weight/Height sorting) and **Ladder Diagram (LD)** for hardware output mapping.
* **Efficiency Algorithms:** Python-side logic that scans the SQL database for the closest empty slot (Load) or the quickest retrieval path (Unload).
* **State Management:** Advanced execution flow using **ENUMs** and **CASE OF** structures for deterministic behavior.

## 🎥 Process Demonstrations

#### 📤 Storage Cycle (Load)
The system identifies the box, applies the weight/height-safety rule, and selects the **nearest optimal slot** to minimize travel time.
*![Load Cycle](Media/Load_GIF.gif)*

#### 📥 Retrieval Cycle (Unload)
Triggered by an HMI request, the WMS identifies the pallet in the database and executes the fastest retrieval sequence to the exit conveyor.
*![Unload Cycle](Media/Unload_GIF.gif)*
