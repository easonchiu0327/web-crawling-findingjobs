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
        public List<Job> JobSelectAll()
        {
            List<Job> jobList = new List<Job>();
            // Directly get the connection string from Web.config
            string connectionString = ConfigurationManager.ConnectionStrings["DefaultConnection"].ConnectionString;

            SqlConnection conn = new SqlConnection(connectionString);
            SqlCommand cmd = new SqlCommand();
            cmd.Connection = conn;
            cmd.CommandText = "SELECT * FROM JobListings";
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
                            (string)reader["Category"],
                            (string)reader["Skills"],
                            (string)reader["Years"],
                            (string)reader["CitizenPR"],
                            (string)reader["Link"]
                        ));
                }
                conn.Close();
            }
            return jobList;
        }

        public List<Job> JobRandomSelect(int rand)
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
                            (string)reader["Category"],
                            (string)reader["Skills"],
                            (string)reader["Years"],
                            (string)reader["CitizenPR"],
                            (string)reader["Link"]
                        ));
                }
                conn.Close();
            }
            return jobList;
        }


    }
}
