using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace web_crawling_findingjobs.JobListLogic.CitizenPR
{
    public class CitizenPR
    {
        private int citizenPR_id;
        private string citizenPR_status;

        public CitizenPR()
        {
        }

        public CitizenPR(int citizenPR_id, string citizenPR)
        {
            this.citizenPR_id = citizenPR_id;
            this.citizenPR_status = citizenPR;
        }

        public int CitizenPR_id { get => citizenPR_id; set => citizenPR_id = value; }
        public string CitizenPR_status { get => citizenPR_status; set => citizenPR_status = value; }
    }
}