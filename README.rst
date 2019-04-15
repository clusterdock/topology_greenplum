==================================
Greenplum topology for clusterdock
==================================

This repository houses the **Greenplum** topology for `clusterdock`_.

.. _clusterdock: https://github.com/clusterdock/clusterdock

Usage
=====

Assuming you've already installed **clusterdock** (if not, go `read the docs`_),
you use this topology by cloning it to a local folder and then running commands
with the ``clusterdock`` script:

.. _read the docs: http://clusterdock.readthedocs.io/en/latest/

.. code-block:: console

    $ git clone https://github.com/clusterdock/topology_greenplum.git
    $ clusterdock start topology_greenplum --namespace streamsets --predictable

To see full usage instructions for the ``start`` action, use ``-h``/``--help``:                                                 

.. code-block:: console

    $ clusterdock start topology_greenplum -h
    clusterdock start topology_greenplum -h
    usage: clusterdock start [--always-pull] [--namespace ns] [--network nw]
                             [-o sys] [-r url] [-h] [--predictable]
                             [--secondary-nodes node [node ...]]
                             [--primary-node node [node ...]]
                             topology

    Start a Greenplum cluster
    
    positional arguments:
      topology              A clusterdock topology directory
    
    optional arguments:
      --always-pull         Pull latest images, even if they're available locally
                            (default: False)
      --namespace ns        Namespace to use when looking for images (default:
                            None)
      --network nw          Docker network to use (default: cluster)
      -o sys, --operating-system sys
                            Operating system to use for cluster nodes (default:
                            None)
      -r url, --registry url
                            Docker Registry from which to pull images (default:
                            docker.io)
      -h, --help            show this help message and exit
    
    Greenplum arguments:
     --predictable         If specified, attempt to expose container ports to the
                            same port number on the host (default: False)
     --greenplum-version   Greenplum database version to use (default: 5.12.0)

    Node groups:
      --primary-node node [node ...]
                            Nodes of the primary-node group. This is master host. (default: ['node-1'])
      --secondary-nodes node [node ...]
                            Nodes of the secondary-nodes group. These are segment hosts. (default:
                            ['node-2', 'node-3'])
