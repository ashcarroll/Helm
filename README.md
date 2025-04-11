# Helm

## Overview
Helm is a streamlined project and team management application built with Django. It provides an intuitive interface for managing projects, tasks, and teams with a focus on simplicity and visual clarity. Helm allows managers to create and oversee projects while team members can view assigned projects, update tasks, and collaborate effectively. The application features a modern, responsive UI built with Bootstrap and enhanced with custom styling.

#### Project Problem Statement:
Managers and Program Managers lose significant time gathering scattered information from multiple tools and places to track team and project health.

#### Project Goal:
A unified dashboard tool to consolidate this data would enable faster decision-making and more time for strategic work.

#### Target Audience:
- People Managers
- Project Managers
- Individual Contributors

---

## Application Features

#### Real-time project status dashboards
Personalised dashboard with metrics relevant to the user such as:
- Owned / Assigned project and task metrics
- Assigned tasks overview
- Visual data on assigned projects and tasks

#### Team management
- Assign users to teams so managers can see all members of their team appropriately
    - Flexible use cases for team management
        - People managers can create and see the ICs that report into them	
        - Project managers can create and see project teams


- Resource management that prevents over allocation and burnout
    - Clearly see how many tasks each IC on a team is assigned to, enabling people managers to make better decisions around resource allocation

 #### Project management and tracking
 - Project creation and management
    - Create projects with clear start and end dates
    - Assign users to project team 


- Progress and status tracking
    - Visually see completion percentage with progress bar
    - View and update status of the project, which will flag on dashboards when appropriate


- Task management
    - See all tasks associated with a project at a glance
    - Manage tasks by updating assignee, details, due dates and status
    - Project Team view
    - View project team and understand how many tasks they are assigned to across all projects


- Project list filtering based on status


#### Profile management
- View and update your user profile
- Customise profile picture
- View your personal activity

---

## Access Instructions
Use this Render.com link to access the site: https://helm-34tp.onrender.com 

Create a new user or log in with either of the following demo accounts to explore the functionality of the site:

<em>Manager:</em> <br>
Username: Eugene.Krabs <br>
Password: @4@YOuABnD

<em>IC:</em> <br>
Username: Mark.Scout <br>
Password: w30Tjyi7z^

---

## User Stories

#### Team Manager Epic:
As a manager I want to effectively manage my team’s health and capacity so that I can develop a high performing team and maintain sustainable delivery

##### Team Manager User Stories:
- As a team manager, I want to view a comprehensive dashboard with team metrics, so that I can quickly assess my team's health and capacity.
- As a team manager, I want to create and manage team structures, so that I can organize my personnel efficiently.
- As a team manager, I want to monitor project progress across my team, so that I can identify and address bottlenecks early.
- As a team manager, I want to view task distribution among team members, so that I can ensure workload is balanced appropriately.
- As a team manager, I want to add, remove, and edit team members, so that I can keep my team roster current.


#### Program / Project Manager Epic:
As a Program / Project Manager I want to ensure the successful delivery of programs of work so that I can deliver business value on time, maintain stakeholder confidence and effectively coordinate across multiple teams and workstreams

##### Project Manager User Stories:
- As a project manager, I want to create new projects with detailed information, so that I can establish clear project parameters from the start.
- As a project manager, I want to set and update project statuses, so that stakeholders have visibility into project health.
- As a project manager, I want to track project completion percentages, so that I can report accurate progress to stakeholders.
- As a project manager, I want to organize tasks into different status categories (Todo, In Progress, Blocked, Done), so that I can visualize workflow stages.
- As a project manager, I want to assign team members to specific tasks, so that responsibilities are clearly defined.
- As a project manager, I want to set and manage project timelines with start and end dates, so that I can ensure projects stay on schedule.


#### IC Epic:
As an IC, I want to effectively manage my work and track my progress so I can deliver my work on time and maintain a sustainable work pace

##### IC User Stories:
- As an IC, I want to view all tasks assigned to me, so that I can prioritize my work effectively.
- As an IC, I want to update the status of my tasks, so that others can see my progress.
- As an IC, I want to view project details I'm involved with, so that I understand the broader context of my work.
- As an IC, I want to see my personal activity summary, so that I can track my contributions over time.
- As an IC, I want to update my profile information, so that my teammates know how to contact me.
- As an IC, I want to view upcoming deadlines for my tasks, so that I can manage my time effectively.

---

## Additional Notes:

The database is also hosted on on Render.com and is being managed using pgAdmin 4 locally, when needed.

For the purposes of this project, everyone has access to all projects as if they are in one tenant or part of the same business. However, if this was a real product on the market, it would be designed as multi-tenant so each business would operate within its own isolated environment, ensuring that data remains private and secure. When a business logs in, they would only see their own projects, teams, and users - never data from other organisations. 



