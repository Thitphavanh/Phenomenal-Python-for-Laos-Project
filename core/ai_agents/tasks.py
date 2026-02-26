"""
Celery Tasks for AI Agents
Asynchronous tasks for long-running operations
ໜ້າວຽກ async ສຳລັບການປະມວນຜົນທີ່ໃຊ້ເວລາດົນ
"""

from celery import shared_task
from django.utils import timezone
from django.contrib.auth.models import User
import logging

from .models import (
    CourseAnalytics,
    PaymentSlipAnalysis,
    CourseRecommendation,
    VectorDocument,
)
from .services.analytics import CourseAnalyticsAgent, BusinessIntelligenceAgent
from .services.payment_slip_processor import PaymentSlipProcessor
from .services.recommendation import CourseRecommendationEngine
from .services.vector_db import VectorDBService
from courses.models import Course
from blog.models import Post
from docs.models import Document as DocsDocument

logger = logging.getLogger(__name__)


# ============================================
# ANALYTICS TASKS
# ============================================

@shared_task(bind=True, max_retries=3)
def generate_course_analytics_task(self, course_id: int):
    """
    Generate analytics for a specific course
    Task ສຳລັບສ້າງການວິເຄາະຂໍ້ມູນຂອງຫຼັກສູດ

    Args:
        course_id (int): ID of the course to analyze

    Returns:
        dict: Analytics results
    """
    try:
        logger.info(f"Starting analytics generation for course {course_id}")

        # Get course
        course = Course.objects.get(id=course_id)

        # Generate analytics
        agent = CourseAnalyticsAgent()
        analytics = agent.analyze_course(course_id)

        if 'error' in analytics:
            logger.error(f"Analytics generation failed: {analytics['error']}")
            return {'status': 'error', 'error': analytics['error']}

        # Mark previous analytics as not current
        CourseAnalytics.objects.filter(course=course).update(is_current=False)

        # Create new analytics
        analytics_obj = CourseAnalytics.objects.create(
            course=course,
            enrollment_prediction=analytics.get('predictions'),
            performance_insights=analytics.get('completion_analysis'),
            student_engagement_score=analytics.get('engagement_score', 0),
            completion_rate_prediction=analytics.get('basic_stats', {}).get('completion_rate', 0),
            recommendations='\n'.join(analytics.get('recommendations', [])),
            suggested_improvements=analytics.get('enrollment_trends'),
            is_current=True
        )

        logger.info(f"Successfully generated analytics for course {course_id}")
        return {
            'status': 'success',
            'analytics_id': analytics_obj.id,
            'course_id': course_id
        }

    except Course.DoesNotExist:
        logger.error(f"Course {course_id} not found")
        return {'status': 'error', 'error': 'Course not found'}

    except Exception as e:
        logger.error(f"Error generating analytics for course {course_id}: {e}")
        # Retry with exponential backoff
        raise self.retry(exc=e, countdown=2 ** self.request.retries)


@shared_task
def generate_all_courses_analytics_task():
    """
    Generate analytics for all published courses
    Task ສຳລັບສ້າງການວິເຄາະຂໍ້ມູນທຸກຫຼັກສູດທີ່ເຜີຍແຜ່

    Returns:
        dict: Summary of results
    """
    try:
        logger.info("Starting analytics generation for all courses")

        courses = Course.objects.filter(is_published=True)
        total = courses.count()
        success_count = 0
        error_count = 0

        for course in courses:
            try:
                generate_course_analytics_task.delay(course.id)
                success_count += 1
            except Exception as e:
                logger.error(f"Failed to queue analytics for course {course.id}: {e}")
                error_count += 1

        logger.info(f"Queued analytics for {success_count}/{total} courses")
        return {
            'status': 'success',
            'total_courses': total,
            'queued': success_count,
            'errors': error_count
        }

    except Exception as e:
        logger.error(f"Error generating all course analytics: {e}")
        return {'status': 'error', 'error': str(e)}


@shared_task
def generate_monthly_bi_report_task():
    """
    Generate monthly Business Intelligence report
    Task ສຳລັບສ້າງລາຍງານ BI ປະຈຳເດືອນ

    Returns:
        dict: BI report data
    """
    try:
        logger.info("Starting monthly BI report generation")

        agent = BusinessIntelligenceAgent()
        report = agent.generate_monthly_report()

        # You could save this to a model if needed
        logger.info("Successfully generated monthly BI report")
        return report

    except Exception as e:
        logger.error(f"Error generating BI report: {e}")
        return {'status': 'error', 'error': str(e)}


# ============================================
# PAYMENT SLIP PROCESSING TASKS
# ============================================

@shared_task(bind=True, max_retries=3)
def process_payment_slip_task(self, analysis_id: int):
    """
    Process payment slip image
    Task ສຳລັບປະມວນຜົນຮູບສະລິບເງິນ

    Args:
        analysis_id (int): ID of PaymentSlipAnalysis object

    Returns:
        dict: Processing results
    """
    try:
        logger.info(f"Starting payment slip processing for analysis {analysis_id}")

        # Get analysis object
        analysis = PaymentSlipAnalysis.objects.get(id=analysis_id)
        analysis.status = 'processing'
        analysis.save()

        # Process slip
        processor = PaymentSlipProcessor()
        result = processor.process_slip(analysis.image.path)

        # Update analysis
        analysis.extracted_data = result.get('extracted_data', {})
        analysis.amount = result.get('extracted_data', {}).get('amount')
        analysis.transaction_id = result.get('extracted_data', {}).get('transaction_id')
        analysis.payment_date = result.get('extracted_data', {}).get('payment_date')
        analysis.sender_name = result.get('extracted_data', {}).get('sender_name')
        analysis.confidence_score = result.get('confidence_score', 0)
        analysis.status = result.get('status', 'completed')
        analysis.processed_at = timezone.now()
        analysis.save()

        logger.info(f"Successfully processed payment slip {analysis_id}")
        return {
            'status': 'success',
            'analysis_id': analysis_id,
            'confidence_score': analysis.confidence_score
        }

    except PaymentSlipAnalysis.DoesNotExist:
        logger.error(f"PaymentSlipAnalysis {analysis_id} not found")
        return {'status': 'error', 'error': 'Analysis not found'}

    except Exception as e:
        logger.error(f"Error processing payment slip {analysis_id}: {e}")

        # Update analysis status
        try:
            analysis = PaymentSlipAnalysis.objects.get(id=analysis_id)
            analysis.status = 'failed'
            analysis.notes = f"Processing error: {str(e)}"
            analysis.save()
        except:
            pass

        # Retry with exponential backoff
        raise self.retry(exc=e, countdown=2 ** self.request.retries)


@shared_task
def process_pending_payment_slips_task():
    """
    Process all pending payment slips
    Task ສຳລັບປະມວນຜົນສະລິບເງິນທີ່ຍັງລໍຖ້າ

    Returns:
        dict: Summary of results
    """
    try:
        logger.info("Starting batch payment slip processing")

        pending_slips = PaymentSlipAnalysis.objects.filter(status='pending')
        total = pending_slips.count()

        for slip in pending_slips:
            process_payment_slip_task.delay(slip.id)

        logger.info(f"Queued {total} payment slips for processing")
        return {
            'status': 'success',
            'total_queued': total
        }

    except Exception as e:
        logger.error(f"Error processing pending payment slips: {e}")
        return {'status': 'error', 'error': str(e)}


# ============================================
# RECOMMENDATION TASKS
# ============================================

@shared_task(bind=True, max_retries=3)
def generate_user_recommendations_task(self, user_id: int, limit: int = 5):
    """
    Generate course recommendations for a user
    Task ສຳລັບສ້າງການແນະນຳຫຼັກສູດສຳລັບຜູ້ໃຊ້

    Args:
        user_id (int): ID of the user
        limit (int): Number of recommendations to generate

    Returns:
        dict: Recommendations results
    """
    try:
        logger.info(f"Starting recommendation generation for user {user_id}")

        # Get user
        user = User.objects.get(id=user_id)

        # Generate recommendations
        engine = CourseRecommendationEngine()
        recommendations = engine.recommend_for_user(user, limit=limit)

        # Mark old recommendations as inactive
        CourseRecommendation.objects.filter(user=user).update(is_active=False)

        # Save new recommendations
        created_count = 0
        for rec in recommendations:
            CourseRecommendation.objects.create(
                user=user,
                recommended_course=rec['course'],
                relevance_score=rec['score'],
                reason=rec['reason'],
                based_on={'method': rec['method']},
                is_active=True
            )
            created_count += 1

        logger.info(f"Successfully generated {created_count} recommendations for user {user_id}")
        return {
            'status': 'success',
            'user_id': user_id,
            'recommendations_count': created_count
        }

    except User.DoesNotExist:
        logger.error(f"User {user_id} not found")
        return {'status': 'error', 'error': 'User not found'}

    except Exception as e:
        logger.error(f"Error generating recommendations for user {user_id}: {e}")
        # Retry with exponential backoff
        raise self.retry(exc=e, countdown=2 ** self.request.retries)


@shared_task
def generate_all_users_recommendations_task():
    """
    Generate recommendations for all active users
    Task ສຳລັບສ້າງການແນະນຳສຳລັບຜູ້ໃຊ້ທຸກຄົນ

    Returns:
        dict: Summary of results
    """
    try:
        logger.info("Starting recommendation generation for all users")

        users = User.objects.filter(is_active=True)
        total = users.count()

        for user in users:
            generate_user_recommendations_task.delay(user.id)

        logger.info(f"Queued recommendations for {total} users")
        return {
            'status': 'success',
            'total_users': total
        }

    except Exception as e:
        logger.error(f"Error generating all user recommendations: {e}")
        return {'status': 'error', 'error': str(e)}


# ============================================
# VECTOR DATABASE TASKS
# ============================================

@shared_task
def populate_vector_database_task():
    """
    Populate vector database with all content
    Task ສຳລັບເພີ່ມຂໍ້ມູນທັງໝົດເຂົ້າ vector database

    Returns:
        dict: Summary of results
    """
    try:
        logger.info("Starting vector database population")

        vector_db = VectorDBService()

        # Add blog posts
        posts = Post.objects.filter(status='published')
        post_docs = []
        post_metadatas = []
        post_ids = []

        for post in posts:
            content = f"{post.title}\n{post.content}"
            post_docs.append(content)
            post_metadatas.append({
                'type': 'blog_post',
                'id': post.id,
                'title': post.title,
                'slug': post.slug,
                'url': f'/blog/{post.slug}/'
            })
            post_ids.append(f"post_{post.id}")

        if post_docs:
            vector_db.add_documents(post_docs, post_metadatas, post_ids)

        # Add courses
        courses = Course.objects.filter(is_published=True)
        course_docs = []
        course_metadatas = []
        course_ids = []

        for course in courses:
            content = f"{course.title}\n{course.description}\n{course.short_description}"
            course_docs.append(content)
            course_metadatas.append({
                'type': 'course',
                'id': course.id,
                'title': course.title,
                'slug': course.slug,
                'url': f'/courses/{course.slug}/'
            })
            course_ids.append(f"course_{course.id}")

        if course_docs:
            vector_db.add_documents(course_docs, course_metadatas, course_ids)

        # Add documentation
        docs = DocsDocument.objects.filter(is_published=True)
        doc_docs = []
        doc_metadatas = []
        doc_ids = []

        for doc in docs:
            content = f"{doc.title}\n{doc.content}"
            doc_docs.append(content)
            doc_metadatas.append({
                'type': 'documentation',
                'id': doc.id,
                'title': doc.title,
                'slug': doc.slug,
                'url': f'/docs/{doc.slug}/'
            })
            doc_ids.append(f"doc_{doc.id}")

        if doc_docs:
            vector_db.add_documents(doc_docs, doc_metadatas, doc_ids)

        total_count = vector_db.get_collection_count()

        logger.info(f"Successfully populated vector database with {total_count} documents")
        return {
            'status': 'success',
            'total_documents': total_count,
            'posts': len(post_docs),
            'courses': len(course_docs),
            'docs': len(doc_docs)
        }

    except Exception as e:
        logger.error(f"Error populating vector database: {e}")
        return {'status': 'error', 'error': str(e)}


@shared_task
def update_vector_document_task(document_type: str, document_id: int):
    """
    Update a single document in vector database
    Task ສຳລັບອັບເດດເອກະສານໜຶ່ງໃນ vector database

    Args:
        document_type (str): Type of document (blog_post, course, documentation)
        document_id (int): ID of the document

    Returns:
        dict: Update results
    """
    try:
        logger.info(f"Updating vector database for {document_type} {document_id}")

        vector_db = VectorDBService()

        content = None
        metadata = None
        doc_id = f"{document_type}_{document_id}"

        # Get document based on type
        if document_type == 'blog_post':
            post = Post.objects.get(id=document_id)
            content = f"{post.title}\n{post.content}"
            metadata = {
                'type': 'blog_post',
                'id': post.id,
                'title': post.title,
                'slug': post.slug,
                'url': f'/blog/{post.slug}/'
            }

        elif document_type == 'course':
            course = Course.objects.get(id=document_id)
            content = f"{course.title}\n{course.description}\n{course.short_description}"
            metadata = {
                'type': 'course',
                'id': course.id,
                'title': course.title,
                'slug': course.slug,
                'url': f'/courses/{course.slug}/'
            }

        elif document_type == 'documentation':
            doc = DocsDocument.objects.get(id=document_id)
            content = f"{doc.title}\n{doc.content}"
            metadata = {
                'type': 'documentation',
                'id': doc.id,
                'title': doc.title,
                'slug': doc.slug,
                'url': f'/docs/{doc.slug}/'
            }

        if content and metadata:
            # Delete old version first
            try:
                vector_db.collection.delete(ids=[doc_id])
            except:
                pass

            # Add new version
            vector_db.add_documents([content], [metadata], [doc_id])

            # Update VectorDocument record
            VectorDocument.objects.update_or_create(
                document_type=document_type,
                document_id=document_id,
                defaults={
                    'content': content,
                    'vector_id': doc_id,
                    'metadata': metadata
                }
            )

        logger.info(f"Successfully updated {document_type} {document_id} in vector database")
        return {
            'status': 'success',
            'document_type': document_type,
            'document_id': document_id
        }

    except Exception as e:
        logger.error(f"Error updating vector document {document_type} {document_id}: {e}")
        return {'status': 'error', 'error': str(e)}


@shared_task
def cleanup_old_analytics_task(days: int = 30):
    """
    Cleanup old analytics records
    Task ສຳລັບລຶບຂໍ້ມູນການວິເຄາະເກົ່າ

    Args:
        days (int): Keep only analytics from last N days

    Returns:
        dict: Cleanup results
    """
    try:
        logger.info(f"Starting cleanup of analytics older than {days} days")

        cutoff_date = timezone.now() - timezone.timedelta(days=days)

        # Delete old analytics (keep current ones)
        deleted_count, _ = CourseAnalytics.objects.filter(
            generated_at__lt=cutoff_date,
            is_current=False
        ).delete()

        logger.info(f"Deleted {deleted_count} old analytics records")
        return {
            'status': 'success',
            'deleted_count': deleted_count
        }

    except Exception as e:
        logger.error(f"Error cleaning up old analytics: {e}")
        return {'status': 'error', 'error': str(e)}


# ============================================
# PERIODIC TASKS (Configure in celery beat)
# ============================================

@shared_task
def daily_tasks():
    """
    Daily maintenance tasks
    Task ປະຈຳວັນ
    """
    logger.info("Running daily maintenance tasks")

    # Generate recommendations for all users
    generate_all_users_recommendations_task.delay()

    # Generate analytics for all courses
    generate_all_courses_analytics_task.delay()

    # Process pending payment slips
    process_pending_payment_slips_task.delay()

    return {'status': 'success', 'message': 'Daily tasks queued'}


@shared_task
def weekly_tasks():
    """
    Weekly maintenance tasks
    Task ປະຈຳອາທິດ
    """
    logger.info("Running weekly maintenance tasks")

    # Cleanup old analytics
    cleanup_old_analytics_task.delay(days=30)

    # Rebuild vector database
    populate_vector_database_task.delay()

    return {'status': 'success', 'message': 'Weekly tasks queued'}


@shared_task
def monthly_tasks():
    """
    Monthly maintenance tasks
    Task ປະຈຳເດືອນ
    """
    logger.info("Running monthly maintenance tasks")

    # Generate BI report
    generate_monthly_bi_report_task.delay()

    return {'status': 'success', 'message': 'Monthly tasks queued'}
