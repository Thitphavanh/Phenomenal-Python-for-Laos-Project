"""
Course Analytics AI Agent
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any
from django.db.models import Count, Avg
from django.utils import timezone
from datetime import timedelta
from courses.models import Course, Enrollment
import logging

logger = logging.getLogger(__name__)


class CourseAnalyticsAgent:
    def analyze_course(self, course_id: int) -> Dict[str, Any]:
        try:
            course = Course.objects.get(id=course_id)
            enrollments = Enrollment.objects.filter(course=course)
            
            # 1. Enrollment Prediction
            prediction = self._predict_enrollments(enrollments)
            
            # 2. Engagement Score
            engagement = self._calculate_engagement(enrollments)
            
            # 3. Recommendations
            recommendations = self._generate_recommendations(engagement, prediction, course)
            
            return {
                'course_id': course.id,
                'course_title': course.title,
                'enrollment_prediction': prediction,
                'engagement_score': engagement,
                'recommendations': recommendations
            }
        except Course.DoesNotExist:
            return {'error': 'Course not found'}

    def _predict_enrollments(self, enrollments) -> Dict[str, int]:
        if not enrollments.exists():
            return {'next_month': 0, 'next_quarter': 0}
            
        # Group by month using pandas
        df = pd.DataFrame(list(enrollments.values('enrolled_at')))
        if df.empty or 'enrolled_at' not in df.columns:
             return {'next_month': 0, 'next_quarter': 0}
             
        df['enrolled_at'] = pd.to_datetime(df['enrolled_at'])
        # Convert to period for monthly grouping
        df['month'] = df['enrolled_at'].dt.to_period('M')
        monthly_counts = df.groupby('month').size()
        
        # Simple linear projection (avg growth last 3 months)
        if len(monthly_counts) < 2:
            avg_growth = 0
            current_monthly = len(enrollments) if len(monthly_counts) == 0 else monthly_counts.iloc[-1]
        else:
            recent = monthly_counts.tail(3)
            # Calculate successive differences
            diffs = recent.diff().dropna()
            avg_growth = diffs.mean() if not diffs.empty else 0
            current_monthly = recent.iloc[-1]
            
        if pd.isna(avg_growth):
            avg_growth = 0
            
        # Simple projection
        next_month = int(max(0, current_monthly + avg_growth))
        # Very rough 3-month projection
        next_quarter = int(max(0, (current_monthly * 3) + (avg_growth * 6)))
        
        return {
            'next_month': next_month,
            'next_quarter': next_quarter
        }

    def _calculate_engagement(self, enrollments) -> float:
        if not enrollments.exists():
            return 0.0
        # Calculate average progress percentage
        avg_progress = enrollments.aggregate(Avg('progress_percentage'))['progress_percentage__avg']
        # Normalize to 0-1 scale
        return round(float(avg_progress or 0) / 100, 2)

    def _generate_recommendations(self, engagement: float, prediction: Dict, course: Course) -> str:
        recs = []
        if engagement < 0.3:
            recs.append("Engagement is low. Consider adding more interactive quizzes or shortening video length.")
        elif engagement > 0.8:
            recs.append("Engagement is excellent! Consider creating an advanced follow-up course.")
            
        if prediction.get('next_month', 0) > 20 and engagement > 0.5:
             recs.append("Growth is trending up. Good time to increase marketing spend.")
             
        if not recs:
            recs.append("Maintain current course structure and monitor feedback.")
            
        return " ".join(recs)


class BusinessIntelligenceAgent:
    def generate_monthly_report(self) -> Dict[str, Any]:
        # Placeholder for BI report
        return {'status': 'ok', 'message': 'Not implemented yet'}
