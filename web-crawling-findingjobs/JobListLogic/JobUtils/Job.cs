using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace web_crawling_findingjobs.JobListLogic.JobUtils
{
    public class Job
    {
        private int id;
        private string companyName;
        private string jobTitle;
        private string location;
        private string link;
        private DateTime createdDate;

        // For Selecting all Jobs
        public Job(int id, string companyName, string jobTitle, string location, string link, DateTime createdDate)
        {
            this.id = id;
            this.companyName = companyName;
            this.jobTitle = jobTitle;
            this.location = location;
            this.link = link;
            this.createdDate = createdDate;
        }

        //Property Accessors
        public int Id { get => id; set => id = value; }
        public string CompanyName { get => companyName; set => companyName = value; }
        public string JobTitle { get => jobTitle; set => jobTitle = value; }
        public string Location { get => location; set => location = value; }
        public string Link { get => link; set => link = value; }
        public DateTime CreatedDate { get => createdDate; set => createdDate = value; }
    }


}