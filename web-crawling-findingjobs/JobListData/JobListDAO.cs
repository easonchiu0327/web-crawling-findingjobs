using System;
using System.Collections.Generic;
using System.Configuration;
using System.Data.SqlClient;
using System.Drawing;
using System.Linq;
using System.Web;
using web_crawling_findingjobs.JobListLogic.JobUtils;

namespace web_crawling_findingjobs.JobListData
{
    public class JobListDAO
    {
        public List<Job> JobSellectAll()
        {
            List<Job> jobList = new List<Job>();
            // Directly get the connection string from Web.config
            string connectionString = ConfigurationManager.ConnectionStrings["DefaultConnection"].ConnectionString;

            SqlConnection conn = new SqlConnection(connectionString);
            SqlCommand cmd = new SqlCommand();
            cmd.Connection = conn;
            cmd.CommandText = "SELECT Id, Company, JobTitle, Location, Link, CreatedAt FROM JobListings";
            using (conn)
            {
                conn.Open();
                SqlDataReader reader = cmd.ExecuteReader();

                while (reader.Read())
                {
                    jobList.Add(
                        new Job(
                            (int)reader["Id"],
                            (string)reader["Company"],
                            (string)reader["JobTitle"],
                            (string)reader["Location"],
                            (string)reader["Link"],
                            (DateTime)reader["CreatedAt"]
                        ));
                }
                conn.Close();
            }
            return jobList;
        }

        public List<Job> JobRandomSellect(int rand)
        {
            List<Job> jobList = new List<Job>();
            // Directly get the connection string from Web.config
            string connectionString = ConfigurationManager.ConnectionStrings["DefaultConnection"].ConnectionString;

            SqlConnection conn = new SqlConnection(connectionString);
            SqlCommand cmd = new SqlCommand();
            cmd.Connection = conn;
            cmd.CommandText = "SELECT TOP 1 * FROM JobListings ORDER BY CHECKSUM(NEWID(), @RandValue)";
            cmd.Parameters.AddWithValue("@RandValue", rand);
            using (conn)
            {
                conn.Open();
                SqlDataReader reader = cmd.ExecuteReader();

                while (reader.Read())
                {
                    jobList.Add(
                        new Job(
                            (int)reader["Id"],
                            (string)reader["Company"],
                            (string)reader["JobTitle"],
                            (string)reader["Location"],
                            (string)reader["Link"],
                            (DateTime)reader["CreatedAt"]
                        ));
                }
                conn.Close();
            }
            return jobList;
        }
    }
}
