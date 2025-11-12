"""
Enhanced Django API Views with Performance Timing
Measures actual grading time for production metrics
"""

import time
import logging
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

# Import your existing models and functions
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Server.api.models import Submission, MarkingScheme, GradingResult
from Server.api.functions import get_markingScheme, grade_submission
from Server.api.serializers import ScoreUpdateSerializer

logger = logging.getLogger(__name__)


class TimedGradeSubmissionView(generics.UpdateAPIView):
    """
    Enhanced version of GradeSubmissionView with detailed timing metrics.
    Use this view to collect performance data for your abstract.
    """
    queryset = Submission.objects.all()
    serializer_class = ScoreUpdateSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        assignment_id = kwargs.get("assignment_id")
        
        # Start total timing
        total_start = time.time()
        
        # Fetch submissions
        fetch_start = time.time()
        submissions = Submission.objects.filter(assignment_id=assignment_id)
        fetch_time = (time.time() - fetch_start) * 1000
        
        # Fetch marking scheme
        scheme_start = time.time()
        marking_scheme = get_markingScheme(assignment_id)
        if not marking_scheme:
            return Response({"error": "Marking scheme not found for this assignment."}, status=404)
        scheme_time = (time.time() - scheme_start) * 1000

        # Grade each submission with individual timing
        scores = []
        grading_times = []
        timing_by_type = {}
        
        for submission in submissions:
            submission_start = time.time()
            
            # Grade the submission
            total_score = grade_submission(submission, marking_scheme)
            
            submission_time = (time.time() - submission_start) * 1000
            grading_times.append(submission_time)
            
            # Get grading results to analyze timing by question type
            grading_results = GradingResult.objects.filter(submission=submission)
            for result in grading_results:
                q_type = result.answer.grading_type if result.answer else "unknown"
                if q_type not in timing_by_type:
                    timing_by_type[q_type] = []
                # Estimate per-answer time (submission_time / number of questions)
                per_answer_time = submission_time / len(grading_results) if grading_results else submission_time
                timing_by_type[q_type].append(per_answer_time)
            
            scores.append({
                "id": submission.id,
                "score": total_score,
                "file_name": submission.file_name,
                "processing_time_ms": round(submission_time, 2)
            })

        total_time = (time.time() - total_start) * 1000

        # Calculate statistics
        avg_grading_time = sum(grading_times) / len(grading_times) if grading_times else 0
        
        timing_stats = {}
        for qtype, times in timing_by_type.items():
            timing_stats[qtype] = {
                'count': len(times),
                'avg_ms': round(sum(times) / len(times), 2),
                'min_ms': round(min(times), 2),
                'max_ms': round(max(times), 2),
                'total_ms': round(sum(times), 2)
            }

        # Log detailed metrics
        logger.info(f"="*60)
        logger.info(f"📊 GRADING PERFORMANCE METRICS - Assignment {assignment_id}")
        logger.info(f"="*60)
        logger.info(f"Database fetch time: {fetch_time:.2f}ms")
        logger.info(f"Marking scheme fetch: {scheme_time:.2f}ms")
        logger.info(f"Total grading time: {sum(grading_times):.2f}ms")
        logger.info(f"Average per file: {avg_grading_time:.2f}ms")
        logger.info(f"Files processed: {len(submissions)}")
        logger.info(f"Total time: {total_time:.2f}ms")
        logger.info(f"-"*60)
        logger.info(f"Timing by question type:")
        for qtype, stats in timing_stats.items():
            logger.info(f"  {qtype}: avg={stats['avg_ms']:.2f}ms, count={stats['count']}")
        logger.info(f"="*60)

        return Response({
            'scores': scores,
            'performance_metrics': {
                'total_time_ms': round(total_time, 2),
                'total_time_seconds': round(total_time / 1000, 2),
                'files_processed': len(submissions),
                'avg_time_per_file_ms': round(avg_grading_time, 2),
                'database_fetch_ms': round(fetch_time, 2),
                'marking_scheme_fetch_ms': round(scheme_time, 2),
                'timing_by_type': timing_stats,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
        })


class SingleAnswerGradingView(APIView):
    """
    API endpoint for grading a single answer with detailed timing.
    Perfect for collecting granular performance metrics by question type.
    
    POST /api/grade-single/
    {
        "student_answer": "Paris",
        "correct_answer": "Paris",
        "question_type": "one_word",
        "question_text": "What is the capital of France?",
        "grading_options": {
            "case_sensitive": false
        }
    }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        start_time = time.time()
        
        try:
            data = request.data
            question_type = data.get('question_type')
            student_answer = data.get('student_answer')
            correct_answer = data.get('correct_answer')
            question_text = data.get('question_text', '')
            grading_options = data.get('grading_options', {})

            # Import grading functions
            from Server.api.functions import is_answer_correct

            # Grade the answer
            grade_start = time.time()
            
            is_correct, score, explanation = is_answer_correct(
                student_answer=student_answer,
                correct_answer=correct_answer,
                grading_type=question_type,
                question_text=question_text,
                grading_options=grading_options
            )
            
            grade_time = (time.time() - grade_start) * 1000
            total_time = (time.time() - start_time) * 1000

            # Log the result
            logger.info(f"⏱️  {question_type} grading: {grade_time:.2f}ms (total: {total_time:.2f}ms)")

            return Response({
                'is_correct': is_correct,
                'score': score,
                'explanation': explanation,
                'question_type': question_type,
                'processing_time_ms': round(grade_time, 2),
                'total_time_ms': round(total_time, 2),
                'overhead_ms': round(total_time - grade_time, 2),
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            })

        except Exception as e:
            total_time = (time.time() - start_time) * 1000
            logger.error(f"❌ Grading error after {total_time:.2f}ms: {str(e)}")
            return Response({
                'error': str(e),
                'processing_time_ms': round(total_time, 2)
            }, status=500)


class PerformanceMetricsView(APIView):
    """
    API endpoint to retrieve aggregated performance metrics.
    
    GET /api/performance-metrics/?assignment_id=123
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        assignment_id = request.query_params.get('assignment_id')
        
        if not assignment_id:
            return Response({'error': 'assignment_id is required'}, status=400)

        try:
            # Get all submissions for the assignment
            submissions = Submission.objects.filter(assignment_id=assignment_id)
            
            # Collect timing data by question type
            timing_by_type = {}
            total_questions = 0
            
            for submission in submissions:
                grading_results = GradingResult.objects.filter(submission=submission)
                
                for result in grading_results:
                    total_questions += 1
                    q_type = result.answer.grading_type if result.answer else "unknown"
                    
                    if q_type not in timing_by_type:
                        timing_by_type[q_type] = {
                            'count': 0,
                            'samples': []
                        }
                    
                    timing_by_type[q_type]['count'] += 1

            # Calculate statistics
            metrics = {
                'assignment_id': assignment_id,
                'total_submissions': submissions.count(),
                'total_questions_graded': total_questions,
                'question_types': timing_by_type,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }

            return Response(metrics)

        except Exception as e:
            logger.error(f"Error retrieving performance metrics: {str(e)}")
            return Response({'error': str(e)}, status=500)
