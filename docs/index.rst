.. CongregationMS documentation master file, created by
   sphinx-quickstart on Wed Nov 20 15:36:26 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to CongregationMS's documentation!
==========================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Introduction
-------------
CongregationMS is a system (a Web Application) that can be used in the operations of one or more Congregations of the Jehovah's Witnesses.

The aim of the system is to use information technology in doing a Congregation's operational tasks.

Easily generate reports such as:
  * Inactive Publishers
  * Regular Pioneers
  * Elders/MS List
  * Monthly Field Service Report
  * and more...

Most prominent feature of the system is the ability to *send via email* a Publisher's Report Card.

Here are the quicklinks:
  * :ref:`initial-setup`
  * :ref:`what-you-can-do`
  * :ref:`how-to`

.. _initial-setup:

Initial setup
-------------
  This section will explain, on first use, how to setup the system as the **Master User** of the system in your Congregation.

  As the Master User, you will be given a user account by the System Admin of your Congregation's CongregationMS instance.

  The account includes your own username and password for authentication. And you will also be given the corresponding role as a Master User.

  Here are the steps:
    * Create the Groups in your congregation.
    * User Accounts.

      - Create user accounts for users who can access your congregation's system.
      - Assign them their corresponding user role.

        + Go to the admin page.
        + Go to ``System > Users`` and select the intended user.
        + Go to the ``Groups`` section and give the appropriate role.

      - Assign them the Groups that they are allowed to access, one by one.

        + Go to the admin page.
        + Go to ``Publishers > User Groups``.
        + Add a record for each group the user is allowed to access.
    * Create Publisher records.

      - If the publisher is a user of the system, or someone who as a User Account, appropriately indicate the user account.
    * Assign created publisher records to their appropriate Groups.
    * Congratulations! You're system is now ready to use. Please refer :ref:`here<what-you-can-do>` to know what you can do with CongregationMS.

.. _what-you-can-do:

What you can do with CongregationMS?
------------------------------------
1. Publishers
^^^^^^^^^^^^^

  Maintain records of publishers.

  Each publisher record can have the following info:
    * Full name
    * Date of Baptism
    * Date of Birth
    * Contact Numbers
    * Elderly
    * Infirmed
    * Assets

      These are assets owned by the publisher that he/she is willing to share the use to the congregation.

      For example: motorcycle, car, truck, video/audio devices, and more.

  What you can do:

    * Assets

      - Create an Asset.
      - View the details of an Asset.
      - Update an Asset.
      - Delete an Asset.


    * Publishers

      - Create a new Publisher.
      - View the details of a Publisher.
      - Update a Publisher.
      - Delete a Publisher

    * Groups

      - Create a new Group
      - View the details of a Group
      - Update a Group and its Members.
      - Delete a Group

2. Pioneering
^^^^^^^^^^^^^
  Maintain records of the pioneers in your congregation.

  In CongregationMS, the term '*Pioneer*' refers to the three different type of pioneers. They can be **Auxillary Pioneers**, **Regular Pioneers**, or **Special Pioneers**.

3. Servants
^^^^^^^^^^^
  Maintain records of the Servants in the Congregation.

  A '*Servant*' is either an **Elder** or a **Ministerial Servant**.

4. Reports
^^^^^^^^^^
  View and download reports.

4.1 Monthly Field Service
"""""""""""""""""""""""""
  Monthly Field Service(MFS) is a sub module of the main module Reports.

  Record publishers' monthly field service reports in this module.

  You can generate the following reports:
    * Publisher's Report Card (MFS History by Publisher)
    * MFS History by Group
  
  And one of the most prominent feature of the CongregationMS is found here: *sharing via email* a Publisher's Report Card.

4.2 Publishers
""""""""""""""
  Generate reports related to Publisher records.

  You can generate the following reports:

    * Infirmed Publishers
    * Elderly Publishers
    * Inactive Publishers

4.3 Pioneering
""""""""""""""
  Generate reports related to the Pioneers of the Congregation.

  You can generate the following reports:

    * Regular Pioneers
    * Auxillary Pioneers
    * Special pioneers

4.4 Servants
""""""""""""
  Generate reports related to the Elders and the Ministerial Servants.

  You can generate the following reports:

    * Elders List
    * Ministerial Servants List

.. _how-to:

How to guides
^^^^^^^^^^^^^
  * How to share via email a Publishers Report Card?

    - Set up user's mailing settings.

      + You can set this up in the admin page ``Mailing > User Mails``.

    - Go to Publishers List
    - Click the ``View MFS History`` button
    - On the MFS history page, click the ``share`` button.
