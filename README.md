# garmin-connect-file-manager

<div align="center">
  
 ![image](https://user-images.githubusercontent.com/78045025/159144654-99ab4f68-eb5f-4819-8806-66761d2037d5.png)

  [![Tweet](https://img.shields.io/twitter/url/https/shields.io.svg?style=social)](https://twitter.com/intent/tweet?text=%F0%9F%93%A2%20Various%20README%20templates%20and%20tips%20on%20writing%20high-quality%20documentation%20that%20people%20want%20to%20read.&url=https://github.com/lucas-nelson-uiuc/garmin-connect-file-manager)
  [![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Flucas-nelson-uiuc%2Fgarmin-connect-file-manager&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)
 [![GitHub stars](https://badgen.net/github/stars/lucas-nelson-uiuc/garmin-connect-file-manager)](https://GitHub.com/lucas-nelson-uiuc/garmin-connect-file-manager)
 [![GitHub issues](https://badgen.net/github/issues/lucas-nelson-uiuc/garmin-connect-file-manager/)](https://GitHub.com/lucas-nelson-uiuc/garmin-connect-file-manager/issues/)
 [![GitHub pull-requests](https://img.shields.io/github/issues-pr/lucas-nelson-uiuc/spotipy_analysis.svg)](https://GitHub.com/lucas-nelson-uiuc/garmin-connect-file-manager/pull/)
 [![Maintenance](https://img.shields.io/badge/Maintained%3F-no-red.svg)](https://GitHub.com/lucas-nelson-uiuc/garmin-connect-file-manager/graphs/commit-activity)

</div>

---


## Table of Contents

- [Introduction](#intro_section)
- [Usage](#usage_section)
- [Next Steps](#next_steps)
- [Project Details](#project_details)


## Introduction <a name = "intro_section"></a>

`Garmin Connect File Manager`, or `gcfm`, is a non-packaged package that allows you to store summary and geographical data from your Garmin Connect activities to your destination of choice. Not only does `gcfm` provide a measure of safety against Garmin server failure, but it also allows you to analyze individual files if you're comfortable doing so. (See [Next Steps](#next_steps) for more.)

## Usage <a name = 'usage_section'></a>

If you're comfortable with Git, feel free to pull this repo straight onto your local computer. If you're not comfortable with Git, after installing it on your computer, copy the SSH and simply `git pull [SSH]` in the directory of choice to get the files seen here.

Once you have a copy of this directory on your local computer, you must first create two separate directories:

- export directory (referred to as `export_dir`): a directory containing folders generated by [gcexport](https://github.com/kjkjava/garmin-connect-export); default functionality relies on the formatting and data gathering of [gcexport](https://github.com/kjkjava/garmin-connect-export), so please look at this repository before completing anything here

- backup directory (referred to as `backup_dir`): a directory that will be the final destination for the activities sitting in `export_dir`

Should everything be in place, an example directory following execution of the `gcfm.py` script will leave you with this tree:

```
# Before running gcfm.py, your directory structure could/should look like this
garmin/
| -- garmin-connect-file-manager/
| -- backup-directory/
| -- export-directory/


# After everything is setup, run the script with the relative paths to backup_dir and export_dir
$ python3 gcfm.py relative/path/to/backup/directory relative/path/to/export/directory


# Let the magic happen and your directory should look like this
garmin/
  ../garmin-connect-file-manager/
  ../backup-directory/
    ../Running/
      -- YYYY-MM-DD-activityID.json
      -- YYYY-MM-DD-activityID.gpx
      ...
    ../Cycling/
      -- YYYY-MM-DD-activityID.json
      -- YYYY-MM-DD-activityID.gpx
      ...
    ...
  ../export-directory/
    -- YYYY-MM-DD_garmin_connect_export/
    -- YYYY-MM-DD_garmin_connect_export/
    ...
```

## Next Steps <a name = "next_steps"></a>

Now that you have the files, what can you do with it? Well, given the time, I would like to create a dashboard that makes use of these files to provide an in-depth view of individual and aggregate activity summaries as well as some neat statistical analyses that I can't come across on that Strava Freemium plan.

Additionally, I'd like to optimize a couple things around here. Runtime isn't a huge concern, but time and storage aren't as cheap for others as it is for this second semester senior, so keep an eye out for *improvements* of the runtime and storage variety.

And, of course, I'm open to recommendations should they filter in.

## Project Details <a name = "project_details"></a>

Author: Lucas Nelson

v-0.0 Completed: 2022/03/19
v-2.0 Completed: 2022/06/15

License: MIT License
