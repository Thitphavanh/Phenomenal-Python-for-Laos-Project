"""
Course Recommendation Engine
ແນະນຳຫຼັກສູດດ້ວຍ Machine Learning
"""

import numpy as np
from typing import List, Dict, Any
from django.contrib.auth.models import User
from courses.models import Course, Enrollment
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging

logger = logging.getLogger(__name__)


class CourseRecommendationEngine:
    """ML-based course recommendation system"""

    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=100, stop_words='english')

    def recommend_for_user(
        self,
        user: User,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Generate personalized course recommendations

        Args:
            user: User object
            limit: Number of recommendations

        Returns:
            List of recommended courses with scores
        """
        try:
            # Get user's enrollment history
            user_enrollments = Enrollment.objects.filter(student=user)
            enrolled_courses = [e.course for e in user_enrollments]

            # Get all available courses
            available_courses = Course.objects.filter(
                status='published'
            ).exclude(
                id__in=[c.id for c in enrolled_courses]
            )

            if not available_courses.exists():
                return []

            # Content-based filtering
            recommendations = self._content_based_filtering(
                enrolled_courses,
                available_courses,
                limit
            )

            # Collaborative filtering (if enough data)
            if user_enrollments.count() > 0:
                collab_recs = self._collaborative_filtering(user, available_courses, limit)
                recommendations = self._merge_recommendations(recommendations, collab_recs)

            return recommendations[:limit]

        except Exception as e:
            logger.error(f"Recommendation error: {e}")
            return []

    def _content_based_filtering(
        self,
        enrolled_courses: List[Course],
        available_courses,
        limit: int
    ) -> List[Dict[str, Any]]:
        """Content-based recommendation using course descriptions"""
        if not enrolled_courses:
            # Return popular courses for new users
            return self._get_popular_courses(available_courses, limit)

        # Build course feature matrix
        all_courses = list(enrolled_courses) + list(available_courses)
        course_texts = [
            f"{c.title} {c.description} {c.short_description}"
            for c in all_courses
        ]

        try:
            # Calculate TF-IDF
            tfidf_matrix = self.vectorizer.fit_transform(course_texts)

            # Calculate similarity
            enrolled_indices = list(range(len(enrolled_courses)))
            available_indices = list(range(len(enrolled_courses), len(all_courses)))

            similarities = cosine_similarity(
                tfidf_matrix[enrolled_indices],
                tfidf_matrix[available_indices]
            )

            # Get average similarity for each available course
            avg_similarities = similarities.mean(axis=0)

            # Get top recommendations
            top_indices = avg_similarities.argsort()[-limit:][::-1]

            recommendations = []
            for idx in top_indices:
                course = available_courses[idx]
                recommendations.append({
                    'course': course,
                    'score': float(avg_similarities[idx]),
                    'reason': f"Similar to courses you've taken",
                    'method': 'content_based'
                })

            return recommendations

        except Exception as e:
            logger.error(f"Content-based filtering error: {e}")
            return self._get_popular_courses(available_courses, limit)

    def _collaborative_filtering(
        self,
        user: User,
        available_courses,
        limit: int
    ) -> List[Dict[str, Any]]:
        """Collaborative filtering based on similar users"""
        # Get users with similar enrollment patterns
        user_enrollments = set(
            Enrollment.objects.filter(student=user).values_list('course_id', flat=True)
        )

        if not user_enrollments:
            return []

        # Find similar users
        similar_users = []
        all_users = User.objects.exclude(id=user.id)

        for other_user in all_users:
            other_enrollments = set(
                Enrollment.objects.filter(student=other_user).values_list('course_id', flat=True)
            )

            # Calculate Jaccard similarity
            if other_enrollments:
                intersection = len(user_enrollments & other_enrollments)
                union = len(user_enrollments | other_enrollments)
                similarity = intersection / union if union > 0 else 0

                if similarity > 0.3:  # Threshold
                    similar_users.append((other_user, similarity))

        # Get courses taken by similar users
        course_scores = {}
        for similar_user, similarity in similar_users:
            their_courses = Enrollment.objects.filter(
                student=similar_user
            ).values_list('course_id', flat=True)

            for course_id in their_courses:
                if course_id not in user_enrollments:
                    course_scores[course_id] = course_scores.get(course_id, 0) + similarity

        # Get top courses
        top_course_ids = sorted(course_scores.items(), key=lambda x: x[1], reverse=True)[:limit]

        recommendations = []
        for course_id, score in top_course_ids:
            try:
                course = Course.objects.get(id=course_id, status='published')
                if course in available_courses:
                    recommendations.append({
                        'course': course,
                        'score': score,
                        'reason': "Students like you also took this course",
                        'method': 'collaborative'
                    })
            except Course.DoesNotExist:
                pass

        return recommendations

    def _get_popular_courses(self, courses, limit: int) -> List[Dict[str, Any]]:
        """Get popular courses based on enrollment count"""
        from django.db.models import Count

        popular = courses.annotate(
            enrollment_count=Count('enrollments')
        ).order_by('-enrollment_count')[:limit]

        return [
            {
                'course': course,
                'score': 0.5,
                'reason': "Popular course with many students",
                'method': 'popularity'
            }
            for course in popular
        ]

    def _merge_recommendations(
        self,
        content_recs: List[Dict],
        collab_recs: List[Dict]
    ) -> List[Dict]:
        """Merge recommendations from different methods"""
        merged = {}

        # Add content-based
        for rec in content_recs:
            course_id = rec['course'].id
            merged[course_id] = rec

        # Add/update with collaborative
        for rec in collab_recs:
            course_id = rec['course'].id
            if course_id in merged:
                # Average the scores
                merged[course_id]['score'] = (merged[course_id]['score'] + rec['score']) / 2
                merged[course_id]['method'] = 'hybrid'
            else:
                merged[course_id] = rec

        # Sort by score
        return sorted(merged.values(), key=lambda x: x['score'], reverse=True)
