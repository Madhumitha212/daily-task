/*Display all the users who enrolled in data warehousing course , score greater than 30 and those
who have sunmitted in february month
*/
SELECT 
u.user_name,
c.course_name,
s.score,
s.Submission_date
FROM Enrollments AS e
INNER JOIN Courses AS c ON e.course_id = c.course_id
INNER JOIN Users As u ON e.user_id = u.user_id
INNER JOIN AssessmentSubmissions AS s ON s.user_id = u.user_id
WHERE c.course_name = 'Data Warehousing' AND s.score > 30 AND DATENAME(month,s.Submission_date) = 'February'

--Find the top 3 ranks based on total score
WITH CTE AS(
SELECT user_id, 
SUM(score) AS Total_score
FROM AssessmentSubmissions AS s
GROUP BY user_id)

SELECT TOP 3
u.user_name,
u.user_id,
c.Total_score,
RANK() OVER(ORDER BY c.Total_score DESC) AS Rank
FROM Users As u
INNER JOIN CTE AS c ON c.user_id = u.user_id;

