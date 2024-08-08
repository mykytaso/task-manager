import os
import random
from datetime import timedelta, datetime

import django


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "it_company_task_manager.settings"
)
django.setup()


from task_manager.models import TaskType, Worker, TaskPriority, Task


def random_date_gen(start_date, end_date):
    delta_days = (end_date - start_date).days
    random_days = random.randint(0, delta_days)
    random_date = start_date + timedelta(days=random_days)
    return random_date.strftime("%Y-%m-%d")


def interact_with_database():
    task_types = TaskType.objects.all()
    workers = Worker.objects.all()
    priorities = TaskPriority.objects.all()
    status = [True, False]

    task_description_list = [
        "Set up and configure the load balancer for "
        "even distribution of traffic.",
        "Implement security measures to protect against common "
        "vulnerabilities.",
        "Create a comprehensive data backup plan for disaster recovery.",
        "Conduct penetration testing to identify potential "
        "security weaknesses.",
        "Design email templates for marketing and transactional messages.",
        "Implement a search functionality for users to easily find content.",
        "Update software dependencies to the latest stable versions.",
        "Set up the development environment with all necessary tools "
        "and libraries.",
        "Conduct usability testing to gather feedback on the user interface.",
        "Create SQL migration scripts to transition to the new "
        "database schema.",
        "Implement user notifications for key events and updates "
        "in the system.",
        "Write a technical blog post explaining a recent feature "
        "or development.",
        "Analyze user feedback to identify areas for improvement.",
        "Develop a reporting module to generate insights from collected data.",
        "Configure SSL certificates to ensure secure communication.",
        "Implement two-factor authentication for enhanced account security.",
        "Create deployment scripts for automating the release process.",
        "Conduct code refactoring to improve code quality "
        "and maintainability.",
        "Set up logging and error tracking to monitor system performance.",
        "Implement file upload functionality for users to share documents."
    ]

    task_name_list = [
        "Develop user authentication module",
        "Design database schema",
        "Implement RESTful API",
        "Write unit tests for login feature",
        "Fix bug in payment processing",
        "Update documentation for API endpoints",
        "Create user interface for dashboard",
        "Optimize database queries",
        "Integrate third-party payment gateway",
        "Conduct code review",
        "Deploy application to staging server",
        "Set up continuous integration pipeline",
        "Research new technologies for project",
        "Configure server monitoring tools",
        "Implement caching mechanism",
        "Migrate data to new database",
        "Design logo and branding",
        "Conduct user acceptance testing",
        "Analyze performance bottlenecks",
        "Create wireframes for new feature",
        "Implement OAuth2 authentication",
        "Fix cross-browser compatibility issues",
        "Refactor legacy codebase",
        "Create API documentation",
        "Develop mobile app interface",
        "Set up load balancer",
        "Implement security measures",
        "Create data backup plan",
        "Conduct penetration testing",
        "Design email templates",
        "Implement search functionality",
        "Update software dependencies",
        "Set up development environment",
        "Conduct usability testing",
        "Create SQL migration scripts",
        "Implement user notifications",
        "Write technical blog post",
        "Analyze user feedback",
        "Develop reporting module",
        "Configure SSL certificates",
        "Implement two-factor authentication",
        "Create deployment scripts",
        "Conduct code refactoring",
        "Set up logging and error tracking",
        "Implement file upload feature",
        "Create marketing website",
        "Develop chatbot functionality",
        "Perform data analysis",
        "Update project roadmap",
        "Automate daily reports",
        "Set up API rate limiting",
        "Design CI/CD pipeline",
        "Optimize image loading",
        "Develop admin panel",
        "Implement password reset feature",
        "Create unit tests for API",
        "Deploy microservices architecture",
        "Implement load testing",
        "Create automated testing scripts",
        "Set up web application firewall",
        "Integrate with CRM system",
        "Create onboarding tutorial",
        "Develop custom analytics dashboard",
        "Implement session management",
        "Set up database replication",
        "Create customer feedback form",
        "Implement single sign-on (SSO)",
        "Optimize mobile responsiveness",
        "Develop browser extension",
        "Implement A/B testing framework",
        "Create marketing automation",
        "Migrate legacy system",
        "Set up OAuth2 integration",
        "Create internal wiki",
        "Develop feature toggle system",
        "Implement role-based access control",
        "Create chatbot training data",
        "Set up automated backups",
        "Design error handling system",
        "Create user segmentation",
        "Implement geolocation services",
        "Set up API documentation site",
        "Optimize network performance",
        "Create payment reconciliation tool",
        "Implement fraud detection",
        "Develop file encryption system",
        "Set up data warehouse",
        "Create push notification service",
        "Integrate social media login",
        "Implement user activity tracking",
        "Create project timelines",
        "Develop feature request form",
        "Implement automated invoicing",
        "Set up feature flag management",
        "Develop data export functionality",
        "Integrate machine learning models",
        "Create API versioning strategy",
        "Implement data validation checks",
        "Set up serverless functions",
        "Create dynamic email templates"
    ]

    for name in task_name_list:

        task = Task(
            name=name,
            description=task_description_list[
                random.randint(0, len(task_description_list) - 1)
            ],
            deadline=random_date_gen(
                datetime(day=15, month=8, year=2024),
                datetime(day=31, month=12, year=2024),
            ),
            is_completed=status[random.randint(0, len(status) - 1)],
            priority=random.choice(priorities),
            task_type=random.choice(task_types),
        )
        task.save()

        random_workers = random.sample(
            list(workers), k=random.randint(1, len(workers))
        )

        task.assignees.set(
            random_workers,
        )


if __name__ == "__main__":
    interact_with_database()
