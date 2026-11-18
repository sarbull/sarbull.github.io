---
title: "How to version a Rails application with a Rake task"
description: "Generate a Rails application version from a .version file and Git revision, then expose it through an initializer in views or controllers."
author: "sarbull"
tags: [rails, deployment]
---

You can expose a Rails application version by combining a `.version` file with the current Git revision. A Rake task writes the result to an initializer, making the version available to views and controllers as `App::Application::VERSION`.

Replace `App` with your application’s module name if it differs. In this example, `.version` lives at the Rails project root (`Rails.root`), and the Rake task belongs in `lib/tasks`. Run the task before loading the generated initializer for the first time.

## Step 1: Create the version file
Create your **.version** file.

**.version**
```
1.0.1
```
## Step 2: Generate the version initializer
Create a rake task that reads that version and generates some ruby code that blends into your rails app.

**lib/tasks/create_version.rake**
```ruby
task :create_version do
  desc "Create version"
  version = File.read("#{Rails.root}/.version").split('.')
  version_file = "#{Rails.root}/config/initializers/version.rb"

  major = version[0]
  minor = version[1]
  patch = version[2]
  build = `git describe --always --tags`

  version_string = "module App
  class Application < Rails::Application
    VERSION = \"#{major.to_s}.#{minor.to_s}.#{patch.to_s}.#{build.strip}\"
  end
end"

  File.open(version_file, "w") {|f| f.print(version_string)}
end
```

## Step 3: Run the Rake task
Run the rake task accordingly to your deploy pipeline or manually but make sure you always commit it.


## Step 4: Inspect the generated version
Check the generated file.

**config/initializers/version.rb**
```ruby
module App
  class Application < Rails::Application
    VERSION = "1.0.1.887f65e"
  end
end
```

## Step 5: Load the initializer
Include your generated version initializer into the main `application.rb` config file.

**config/application.rb**
```ruby
...
require_relative "initializers/version"
...
```

## Step 6: Display the application version
Print it wherever you need it, in the views or maybe in a controller.

```ruby
My version: <%= App::Application::VERSION %>
```

For the surrounding build and release process, see [from zero to production]({% post_url 2017-01-10-from-zero-to-production %}).
