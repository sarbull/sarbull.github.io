---
title: "From zero to production: a web application release checklist"
description: "Plan a web application release with version control, separate environments, automated builds, and an early deployment of a minimal application."
author: "sarbull"
tags: [deployment]
---

Production is the environment where customers access your application. Before building the first feature, I prefer to establish version control, separate environments, automated builds, and a repeatable deployment process. Deploying a minimal “Hello World” application first exercises that path before the project becomes more complex.

## Plan the application and its dependencies

Create a rough architecture plan for how the components will interact. Choose technologies for the requirements of the project and the experience of the team. A microservice architecture still needs those choices; it also introduces service boundaries and operational work.

## Put the project in version control

Track the application in Git or another version control system from the beginning. A recorded revision makes it easier to connect a deployed version to its source and to review changes before release.

For Rails, I use [a Rake task to generate the application version]({% post_url 2025-01-28-how-to-version-my-rails-application %}) from a version file and the Git revision.

## Separate development, test, and production

Set up development, test, and production environments so you can develop the application, check its behavior, and then release it to customers. Keep environment-specific configuration separate from the application code.

## Automate builds and checks

Configure a build agent to run the build, unit tests, and integration tests when the project changes. The results should tell the team whether a revision can still be built and whether the checks passed.

Automating repetitive deployment steps also reduces opportunities for manual errors. The exact checks and release process depend on the application.

## Deploy a minimal application first

After creating the basic architecture and build setup, deploy “Hello World” to production. This confirms that the initial build, configuration, and deployment path works; it does not prove the complete application is stable or ready for traffic.

From that first successful release, build and deploy the first feature through the same cycle. For a self-hosted example, see [setting up Dokku on DigitalOcean]({% post_url 2017-01-17-create-your-own-paas-with-dokku-and-digitalocean %}).
