Propagation
===========

The orbit propagation computes the satellites states foward or backward in time for a given initial state. The results are stored internally in binary interpolation files (`.ipf`). More information on these files can be found in the GODOT documentation.

Propagation requests
^^^^^^^^^^^^^^^^^^^^

.. mermaid::

    sequenceDiagram
        actor User
        participant COFY
        participant Worker
        participant Cache
        participant FDB as Large file storage
        participant RDB as Relational database


        User->>COFY: Propagation request data;
        activate COFY
        COFY->>COFY: validate request
        COFY->>User: Propagation request accepted (202 ACCEPTED);
        COFY->>Worker: Propagation request data;
        deactivate COFY
        activate Worker
        Worker->>Worker: perform orbit propagation

        Worker->>FDB: generated ipf file

        Worker->>RDB: orbit propagation status
        deactivate Worker


Propagation status
^^^^^^^^^^^^^^^^^^

Furthermore, during the time the


The workers have a queue of tasks and only can process a limited number of jobs simultaneously. Adding more workers increases the capacity of the application.
