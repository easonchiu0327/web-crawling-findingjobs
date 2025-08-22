using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace web_crawling_findingjobs.JobListLogic.JobUtils
{
    public class Job
    {
        private int id;
        private string company;
        private string jobTitle;
        private string location;
        private string category;
        private string skills;
        private string years;
        private string citizenPR;
        private string link;
        

        // For Selecting all Jobs
        public Job(int id, string company, string jobTitle, string location, string category, string skills, string years, string citizenPR, string link)
        {
            this.id = id;
            this.company = company;
            this.jobTitle = jobTitle;
            this.location = location;
            this.category = category;
            this.skills = skills;
            this.years = years;
            this.citizenPR = citizenPR;
            this.link = link;
            
        }

        //Property Accessors
        public int Id { get => id; set => id = value; }
        public string Company { get => company; set => company = value; }
        public string JobTitle { get => jobTitle; set => jobTitle = value; }
        public string Location { get => location; set => location = value; }
        public string Category { get => category; set => category = value; }
        public string Skills { get => skills;   set => skills = value; }
        public string Years { get => years; set => years = value; }
        public string CitizenPR { get => citizenPR; set => citizenPR = value; }
        public string Link { get => link; set => link = value; }
    }


}